#!/usr/bin/env bash

echo "Running configure.sh"

adminUsername=$1
adminPassword=$2

# This is all to figure out what our rally point is.  There might be a much better way to do this.

region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.region'  \
  | sed 's/^"\(.*\)"$/\1/' )

instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.instanceId' \
  | sed 's/^"\(.*\)"$/\1/' )

autoscalingGroup=$(aws ec2 describe-instances \
  --region ${region} \
  --instance-ids ${instanceID} \
  | jq '.Reservations[0]|.Instances[0]|.Tags[] | select( .Key == "aws:autoscaling:groupName") | .Value' \
  | sed 's/^"\(.*\)"$/\1/' )

autoscalingGroupInstanceIDs=$(aws autoscaling describe-auto-scaling-groups \
  --region ${region} \
  --query 'AutoScalingGroups[*].Instances[*].InstanceId' \
  --auto-scaling-group-name ${autoscalingGroup} \
  | grep "i-" | sed 's/ //g' | sed 's/"//g' |sed 's/,//g' | sort)

rallyInstanceID=`echo ${autoscalingGroupInstanceIDs} | cut -d " " -f1`

rallyPrivateDNS=$(aws ec2 describe-instances \
  --region ${region} \
  --query  'Reservations[0].Instances[0].NetworkInterfaces[0].PrivateIpAddresses[0].PrivateDnsName' \
  --instance-ids ${rallyInstanceID} \
  --output text)

nodePrivateDNS=`curl http://169.254.169.254/latest/meta-data/local-hostname`

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'
echo rallyPrivateDNS \'$rallyPrivateDNS\'
echo nodePrivateDNS \'$nodePrivateDNS\'

cd /opt/couchbase/bin/

echo "Running couchbase-cli node-init"
output=""
while [[ ! $output =~ "SUCCESS" ]]
do
  output=`./couchbase-cli node-init \
    --cluster=$nodePrivateDNS \
    --node-init-hostname=$nodePrivateDNS \
    --node-init-data-path=/datadisks/disk1/data \
    --node-init-index-path=/datadisks/disk1/index \
    --user=$adminUsername \
    --pass=$adminPassword`
  echo node-init output \'$output\'
  sleep 10
done

if [[ $rallyPrivateDNS == $nodePrivateDNS ]]
then
  totalRAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  dataRAM=$((50 * $totalRAM / 100000))
  indexRAM=$((15 * $totalRAM / 100000))

  echo "Running couchbase-cli cluster-init"
  ./couchbase-cli cluster-init \
    --cluster=$nodePrivateDNS \
    --cluster-ramsize=$dataRAM \
    --cluster-index-ramsize=$indexRAM \
    --cluster-username=$adminUsername \
    --cluster-password=$adminPassword \
    --services=data,index,query,fts
else
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "Server $nodePrivateDNS:8091 added" && ! $output =~ "Node is already part of cluster." ]]
  do
    output=`./couchbase-cli server-add \
      --cluster=$rallyPrivateDNS \
      --user=$adminUsername \
      --pass=$adminPassword \
      --server-add=$nodePrivateDNS \
      --server-add-username=$adminUsername \
      --server-add-password=$adminPassword \
      --services=data,index,query,fts`
    echo server-add output \'$output\'
    sleep 10
  done

  echo "Running couchbase-cli rebalance"
  output=""
  while [[ ! $output =~ "SUCCESS" ]]
  do
    output=`./couchbase-cli rebalance \
    --cluster=$rallyPrivateDNS \
    --user=$adminUsername \
    --pass=$adminPassword`
    echo rebalance output \'$output\'
    sleep 10
  done

fi
