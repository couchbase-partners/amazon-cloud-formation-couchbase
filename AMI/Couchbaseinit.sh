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
		-d datanode count
		-i indexnode count
		-q querynode count
		-m mds mode
EOF
	exit 1
}

# ------------------------------------------------------------------
#          Read all inputs
# ------------------------------------------------------------------


while getopts ":h:u:p:d:q:i:m:" o; do
    case "${o}" in
        h) usage && exit 0
			;;
		p) PASSWORD=${OPTARG}
			;;
		u) ADMIN=${OPTARG}
			;;
   		d) #Couchbase datanode count
      		DATA_NODE=${OPTARG}
      		;;
    	q)  
      		QUERY_NODE=${OPTARG}
      		;;
    	i) 
    		INDEX_NODE=${OPTARG}
      		;;
      	m)
    		MDS=${OPTARG}
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

echo "USER_NAME", $ADMIN >> /home/ec2-user/instances.txt
echo "PASSWORD", $PASSWORD >> /home/ec2-user/instances.txt
echo "DATA_NODE", $DATA_NODE >>   /home/ec2-user/instances.txt
echo "INDEX_NODE", $INDEX_NODE >> /home/ec2-user/instances.txt
echo "QUERY_NODE", $QUERY_NODE >> /home/ec2-user/instances.txt
echo "MDS_MODE", $MDS >> /home/ec2-user/instances.txt

for id in ${INSTANCES_IN_ASG}
do
	MYROLE=${INSTANCE2ROLE[${id}]}
	if [ "${MYROLE}" == "master" ]; then

		echo "master", $MASTER_DNS >> /home/ec2-user/instances.txt	
	else
		WORKER_DNS=${INSTANCE2DNS[${id}]}
		echo "slave", $WORKER_DNS >> /home/ec2-user/instances.txt
	fi
done

chmod 777 /home/ec2-user/instances.txt
python cluster.py
rm -rf /home/ec2-user/instances.txt

