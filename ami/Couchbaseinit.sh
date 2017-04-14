 #!/bin/bash

# ------------------------------------------------------------------
#        Discover Instances within AutoScaling Group
#		 Note: Instance need to be able to use AWS CLI as below
#		 Make sure Instance Profile permits these call (if IAM is used)
#			-  aws ec2 describe-instances
#			-  aws autoscaling describe-auto-scaling-groups 
# ------------------------------------------------------------------


usage() {
	cat <<EOF
	Usage: $0 [options]
		-h print usage
		-u admin
		-p password
EOF
	exit 1
}

# ------------------------------------------------------------------
#          Read all inputs
# ------------------------------------------------------------------


while getopts ":h:u:p:" o; do
    case "${o}" in
        h) usage && exit 0
			;;
		p) PASSWORD=${OPTARG}
			;;
		u) ADMIN=${OPTARG}
			;;
       	*)
            usage
            ;;
    esac
done

[[ -z "$PASSWORD" ]]  && echo "Input password missing" && usage;
[[ -z "$ADMIN" ]]  && echo "Input admin user missing" && usage;


export LANG="en_US.UTF-8"
export LANGUAGE="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
export LC_NUMERIC="en_US.UTF-8"
export LC_TIME="en_US.UTF-8"
export LC_COLLATE="en_US.UTF-8"
export LC_MONETARY="en_US.UTF-8"
export LC_MESSAGES="en_US.UTF-8"
export LC_PAPER="en_US.UTF-8"
export LC_NAME="en_US.UTF-8"
export LC_ADDRESS="en_US.UTF-8"
export LC_TELEPHONE="en_US.UTF-8"
export LC_MEASUREMENT="en_US.UTF-8"
export LC_IDENTIFICATION="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"


declare -A INSTANCE2DNS
declare -A INSTANCE2IP
declare -A INSTANCE2ROLE
declare -A INSTANCE2INDEX

#ADMIN=Administrator
#PASSWORD=password



# ------------------------------------------------------------------
#				Uses jq to parse JSON
# ------------------------------------------------------------------


[ -z ${JQ_COMMAND} ] && export JQ_COMMAND=/tmp/jq
if [ ! -x {JQ_COMMAND} ]; then
	wget -q https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 -O /tmp/jq
	chmod 755 /tmp/jq
fi


echo "Discovering nodes..."

export PATH=${PATH}:/sbin:/usr/sbin:/usr/local/sbin:/root/bin:/usr/local/bin:/usr/bin:/bin:/usr/bin/X11:/usr/X11R6/bin:/usr/games:/usr/lib/AmazonEC2/ec2-api-tools/bin:/usr/lib/AmazonEC2/ec2-ami-tools/bin:/usr/lib/mit/bin:/usr/lib/mit/sbin

if [ -z ${AWS_DEFAULT_REGION} ]; then
	 export AWS_DEFAULT_REGION=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
					| ${JQ_COMMAND} '.region'  \
					| sed 's/^"\(.*\)"$/\1/' )
fi
if [ -z ${AWS_DEFAULT_AVAILABILITY_ZONE} ]; then
	 export AWS_DEFAULT_AVAILABILITY_ZONE=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
						| ${JQ_COMMAND} '.availabilityZone' \
						| sed 's/^"\(.*\)"$/\1/' )
fi

if [ -z ${AWS_INSTANCEID} ]; then
	 export AWS_INSTANCEID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
						| ${JQ_COMMAND} '.instanceId' \
						| sed 's/^"\(.*\)"$/\1/' )
fi


MY_PUBLIC_DNS=$(/usr/local/bin/aws ec2 describe-instances --instance-ids ${AWS_INSTANCEID} \
				| ${JQ_COMMAND} '.Reservations[0]|.Instances[0]|.PublicDnsName' \
				| sed 's/^"\(.*\)"$/\1/' )


MY_AUTOSCALING_GROUP=$(/usr/local/bin/aws ec2 describe-instances --instance-ids ${AWS_INSTANCEID} \
						| ${JQ_COMMAND} '.Reservations[0]|.Instances[0]|.Tags[] | select( .Key == "aws:autoscaling:groupName") | .Value' \
						| sed 's/^"\(.*\)"$/\1/' )


INSTANCES_IN_ASG=$(/usr/local/bin/aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[*].Instances[*].InstanceId' --auto-scaling-group-name ${MY_AUTOSCALING_GROUP} \
				| grep "i-" | sed 's/ //g' | sed 's/"//g' |sed 's/,//g' | sort)


MY_STACK_NAME=$(/usr/local/bin/aws ec2 describe-instances --instance-id ${AWS_INSTANCEID} --region ${AWS_DEFAULT_REGION} \
				--query 'Reservations[*].Instances[*].Tags[][]' \
				|  ${JQ_COMMAND} '.[]|select(.Key == "aws:cloudformation:stack-name") | .Value' | sed 's/"//g')



# INSTANCES_IN_ASG is sorted based on EC2 instance ID
# self nominate the first ID to be master

MASTER_NODE_SET=
MASTER_NODE_INSTANCE=
MASTER_DNS=
# pick first one
INDEX=0
for id in ${INSTANCES_IN_ASG}
do
	INSTANCE2INDEX[${id}]=${INDEX}
	let INDEX=INDEX+1
	if [ -z ${MASTER_NODE_SET} ]; then
		MASTER_NODE_SET=$id
		MASTER_NODE_INSTANCE=$id
		INSTANCE2ROLE[${id}]="master"
		MASTER_DNS=$(/usr/local/bin/aws ec2 describe-instances --instance-ids ${id} \
					| ${JQ_COMMAND} '.Reservations[0]|.Instances[0]|.PublicDnsName' \
					| sed 's/^"\(.*\)"$/\1/' )				
	else
		INSTANCE2ROLE[${id}]="worker"
	fi
	DNS=$(/usr/local/bin/aws ec2 describe-instances --instance-ids ${id} \
				| ${JQ_COMMAND} '.Reservations[0]|.Instances[0]|.PublicDnsName' \
				| sed 's/^"\(.*\)"$/\1/' )				
	INSTANCE2DNS[${id}]=${DNS}

	PRIVATE_IP=$(/usr/local/bin/aws ec2 describe-instances --instance-ids ${id} \
				 --region ${AWS_DEFAULT_REGION} \
				 --query  'Reservations[*].Instances[*].NetworkInterfaces[*].PrivateIpAddresses[0].PrivateIpAddress[][0]' \
				 --output text)
	INSTANCE2IP[${id}]=${PRIVATE_IP}

done


# ------------------------------------------------------------------
#				Print All Info
# ------------------------------------------------------------------

echo "Printing Instances in AutoScaling Group ${MY_AUTOSCALING_GROUP}"
for id in ${INSTANCES_IN_ASG}
do
	echo ${id}:${INSTANCE2ROLE[${id}]}:${INSTANCE2DNS[${id}]}:${INSTANCE2INDEX[${id}]}:${INSTANCE2IP[${id}]}
done


COUCHBASE_CLI=/opt/couchbase/bin/couchbase-cli

if [ "$MASTER_NODE_INSTANCE" != "${AWS_INSTANCEID}" ];then
	exit 0
fi

# ------------------------------------------------------------------
#       Only master node should rest of the script
# ------------------------------------------------------------------


for id in ${INSTANCES_IN_ASG}
do
	MYROLE=${INSTANCE2ROLE[${id}]}
	if [ "${MYROLE}" == "master" ]; then
		curl -v -X POST http://$MASTER_DNS:8091/pools/default -d memoryQuota=300 -d indexMemoryQuota=300
		curl -v http://$MASTER_DNS:8091/node/controller/setupServices -d services=kv%2Cn1ql%2Cindex
		curl -v http://$MASTER_DNS:8091/settings/web -d port=8091 -d username=${ADMIN} -d password=${PASSWORD}
		sleep 60
		#curl -v -u ${ADMIN}:${PASSWORD} -X POST http://$MASTER_DNS:8091/sampleBuckets/install -d '["travel-sample"]'		
	else
		WORKER_DNS=${INSTANCE2DNS[${id}]}
		WORKER_IP=${INSTANCE2IP[${id}]}
		PARAMETER="hostname=${WORKER_IP}&user=${ADMIN}&password=${PASSWORD}"
		curl -v http://$WORKER_DNS:8091/node/controller/setupServices -d services=kv%2Cn1ql%2Cindex
                curl -v http://$WORKER_DNS:8091/settings/web -d port=8091 -d username=${ADMIN} -d password=${PASSWORD}
        curl -u ${ADMIN}:${PASSWORD}  http://$WORKER_DNS:8091/pools/default
        curl -u ${ADMIN}:${PASSWORD}  http://$MASTER_DNS:8091/pools/default 
        curl -u ${ADMIN}:${PASSWORD}  http://$WORKER_DNS:8091/pools/default/buckets/  
        curl -u ${ADMIN}:${PASSWORD}  http://$MASTER_DNS:8091/pools/default/buckets/      
        sleep 120        
        COMMAND=$(echo curl -u ${ADMIN}:${PASSWORD} "http://${MASTER_DNS}:8091/controller/addNode" -d ${PARAMETER})
        echo ${COMMAND}
        ${COMMAND}
	fi
done


# ------------------------------------------------------------------
#       Rebalance Couchbase nodes
# ------------------------------------------------------------------


KNOWN_NODES=
for id in ${INSTANCES_IN_ASG}
do
	MYIP=${INSTANCE2IP[${id}]}
	KNOWN_NODES="ns_1@"$(echo ${MYIP}),${KNOWN_NODES}
done

sleep 120
COMMAND=$(echo curl -v -u ${ADMIN}:${PASSWORD} -X POST "http://$MASTER_DNS:8091/controller/rebalance" -d  "knownNodes=${KNOWN_NODES}")
echo ${COMMAND}
sleep 60
${COMMAND}
curl -u ${ADMIN}:${PASSWORD} "http://$MASTER_DNS:8091/pools/default/rebalanceProgress"
curl -u ${ADMIN}:${PASSWORD} "http://$MASTER_DNS:8091/pools/default/tasks"



