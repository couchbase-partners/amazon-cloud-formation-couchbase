#!/usr/bin/env bash

echo "Running syncGateway.sh"

stackName=$1
rallyAutoScalingGroup=$2

yum -y update
yum -y install jq
source util.sh
rallyPublicDNS=`getRallyPublicDNS ${rallyAutoScalingGroup}`

region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.region'  \
  | sed 's/^"\(.*\)"$/\1/' )

instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.instanceId' \
  | sed 's/^"\(.*\)"$/\1/' )

echo "Using the settings:"
echo stackName \'$stackName\'
echo rallyAutoScalingGroup \'$rallyAutoScalingGroup\'
echo rallyPublicDNS \'$rallyPublicDNS\'
echo region \'$region\'
echo instanceID \'$instanceID\'

aws ec2 create-tags \
  --region ${region} \
  --resources ${instanceID} \
  --tags Key=Name,Value=${stackName}-SyncGateway

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
