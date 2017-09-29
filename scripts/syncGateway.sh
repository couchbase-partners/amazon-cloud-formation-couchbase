#!/usr/bin/env bash

echo "Running syncGateway.sh"

license=$1
stackName=$2

yum -y update
yum -y install jq

if [[ $license == "None" ]]
then
  wget https://packages.couchbase.com/releases/couchbase-sync-gateway/1.4.1/couchbase-sync-gateway-enterprise_1.4.1-3_x86_64.rpm
  rpm -i couchbase-sync-gateway-enterprise_1.4.1-3_x86_64.rpm
fi

region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.region'  \
  | sed 's/^"\(.*\)"$/\1/' )

instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.instanceId' \
  | sed 's/^"\(.*\)"$/\1/' )

echo "Using the settings:"
echo stackName \'$stackName\'
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
  "log": ["*"]
}
' > ${file}
chmod 755 ${file}
chown sync_gateway ${file}
chgrp sync_gateway ${file}

# Need to restart to load the changes
service sync_gateway stop
service sync_gateway start
