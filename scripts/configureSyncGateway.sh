#!/usr/bin/env bash

echo "Running configureSyncGateway.sh"

serverAutoScalingGroup=$1

# This is all to figure out what our rally point is.  There might be a much better way to do this.
yum -y install jq

region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.region'  \
  | sed 's/^"\(.*\)"$/\1/' )

instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
    | jq '.instanceId' \
    | sed 's/^"\(.*\)"$/\1/' )

serverAutoscalingGroupInstanceIDs=$(aws autoscaling describe-auto-scaling-groups \
  --region ${region} \
  --query 'AutoScalingGroups[*].Instances[*].InstanceId' \
  --auto-scaling-group-name ${serverAutoScalingGroup} \
  | grep "i-" | sed 's/ //g' | sed 's/"//g' |sed 's/,//g' | sort)

rallyInstanceID=`echo ${serverAutoscalingGroupInstanceIDs} | cut -d " " -f1`

rallyPublicDNS=$(aws ec2 describe-instances \
    --region ${region} \
    --query  'Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicDnsName' \
    --instance-ids ${rallyInstanceID} \
    --output text)

nodePublicDNS=`curl http://169.254.169.254/latest/meta-data/public-hostname`

echo "Using the settings:"
echo serverAutoScalingGroup \'$serverAutoScalingGroup\'
echo rallyPublicDNS \'$rallyPublicDNS\'
echo nodePublicDNS \'$nodePublicDNS\'
echo instanceID \'$instanceID\'

aws ec2 create-tags --resources ${instanceID} --tags Key=Name,Value=SyncGateway

file="/opt/sync_gateway/etc/sync_gateway.json"
echo '
{
  "interface": "0.0.0.0:4984",
  "adminInterface": "0.0.0.0:4985",
  "log": ["*"],
  "databases": {
    "database": {
      "server": "http://'${rallyPublicDNS}':8091",
      "bucket": "sync_gateway",
      "users": {
        "GUEST": { "disabled": false, "admin_channels": ["*"] }
      }
    }
  }
}
' > ${file}
chmod 755 ${file}
chown sync_gateway ${file}
chgrp sync_gateway ${file}

# Need to restart to load the changes
service sync_gateway stop
service sync_gateway start
