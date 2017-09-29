#!/usr/bin/env bash

echo "Running server.sh"

license=$1
adminUsername=$2
adminPassword=$3
services=$4
stackName=$5

yum -y update
yum -y install jq

if [[ $license == "None" ]]
then
  wget https://packages.couchbase.com/releases/5.0.0/couchbase-server-enterprise-5.0.0-centos6.x86_64.rpm
  rpm --install couchbase-server-enterprise-5.0.0-centos6.x86_64.rpm
fi

source util.sh
formatDataDisk
turnOffTransparentHugepages
setSwappinessToZero

if [ -z "$6" ]
then
  echo "This node is part of the autoscaling group that contains the rally point."
  rallyPublicDNS=`getRallyPublicDNS`
else
  rallyAutoScalingGroup=$6
  echo "This node is not the rally point and not part of the autoscaling group that contains the rally point."
  echo rallyAutoScalingGroup \'$rallyAutoScalingGroup\'
  rallyPublicDNS=`getRallyPublicDNS ${rallyAutoScalingGroup}`
fi

region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.region'  \
  | sed 's/^"\(.*\)"$/\1/' )

instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
  | jq '.instanceId' \
  | sed 's/^"\(.*\)"$/\1/' )

nodePublicDNS=`curl http://169.254.169.254/latest/meta-data/public-hostname`

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'
echo services \'$services\'
echo stackName \'$stackName\'
echo rallyPublicDNS \'$rallyPublicDNS\'
echo region \'$region\'
echo instanceID \'$instanceID\'
echo nodePublicDNS \'$nodePublicDNS\'

if [[ ${rallyPublicDNS} == ${nodePublicDNS} ]]
then
  aws ec2 create-tags \
    --region ${region} \
    --resources ${instanceID} \
    --tags Key=Name,Value=${stackName}-ServerRally
else
  aws ec2 create-tags \
    --region ${region} \
    --resources ${instanceID} \
    --tags Key=Name,Value=${stackName}-Server
fi

cd /opt/couchbase/bin/

echo "Running couchbase-cli node-init"
output=""
while [[ ! $output =~ "SUCCESS" ]]
do
  output=`./couchbase-cli node-init \
    --cluster=$nodePublicDNS \
    --node-init-hostname=$nodePublicDNS \
    --node-init-data-path=/mnt/datadisk/data \
    --node-init-index-path=/mnt/datadisk/index \
    --user=$adminUsername \
    --pass=$adminPassword`
  echo node-init output \'$output\'
  sleep 10
done

if [[ $rallyPublicDNS == $nodePublicDNS ]]
then
  totalRAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  dataRAM=$((50 * $totalRAM / 100000))
  indexRAM=$((25 * $totalRAM / 100000))

  echo "Running couchbase-cli cluster-init"
  ./couchbase-cli cluster-init \
    --cluster=$nodePublicDNS \
    --cluster-username=$adminUsername \
    --cluster-password=$adminPassword \
    --cluster-ramsize=$dataRAM \
    --cluster-index-ramsize=$indexRAM \
    --services=${services}
else
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "Server $nodePublicDNS:8091 added" && ! $output =~ "Node is already part of cluster." ]]
  do
    output=`./couchbase-cli server-add \
      --cluster=$rallyPublicDNS \
      --user=$adminUsername \
      --pass=$adminPassword \
      --server-add=$nodePublicDNS \
      --server-add-username=$adminUsername \
      --server-add-password=$adminPassword \
      --services=${services}`
    echo server-add output \'$output\'
    sleep 10
  done

  echo "Running couchbase-cli rebalance"
  output=""
  while [[ ! $output =~ "SUCCESS" ]]
  do
    output=`./couchbase-cli rebalance \
    --cluster=$rallyPublicDNS \
    --user=$adminUsername \
    --pass=$adminPassword`
    echo rebalance output \'$output\'
    sleep 10
  done

fi
