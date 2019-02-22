#!/usr/bin/env bash
#TODO: add tag when through util.sh to instance when completed.
#TODO: remove or make tag false when terminating -- optional
#TODO: possibly do not need to pass the stackName
#TODO: possibly do not need to pass the autoscaling group
echo "Running server.sh"

adminUsername=$1
adminPassword=$2
services=$3
stackName=$4
version=$5

echo "Got the parameters:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'
echo services \'$services\'
echo stackName \'$stackName\'
echo version \'$version\'

#######################################################"
############## Install Couchbase Server ###############"
#######################################################"
echo "Installing Couchbase Server..."

wget https://packages.couchbase.com/releases/${version}/couchbase-server-enterprise-${version}-centos6.x86_64.rpm
rpm --install couchbase-server-enterprise-${version}-centos6.x86_64.rpm

#######################################################"
############ Turn Off Transparent Hugepages ###########"
#######################################################"
echo "Turning off transparent hugepages..."

echo "#!/bin/bash
### BEGIN INIT INFO
# Provides:          disable-thp
# Required-Start:    $local_fs
# Required-Stop:
# X-Start-Before:    couchbase-server
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Disable THP
# Description:       disables Transparent Huge Pages (THP) on boot
### END INIT INFO
echo 'never' > /sys/kernel/mm/transparent_hugepage/enabled
echo 'never' > /sys/kernel/mm/transparent_hugepage/defrag
" > /etc/init.d/disable-thp
chmod 755 /etc/init.d/disable-thp
service disable-thp start
chkconfig disable-thp on

#######################################################
################# Set Swappiness to 0 #################
#######################################################
echo "Setting swappiness to 0..."

sysctl vm.swappiness=0
echo "
# Required for Couchbase
vm.swappiness = 0
" >> /etc/sysctl.conf

source util.sh
formatDataDisk

#All servers are now rally servers after they are added to the cluster.  Initially there is one pre-defined ally server when the cluster is being init.


region=$(getRegion)
instanceID=$(getInstanceID)
nodePrivateIP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)

isRally $instanceID
if isRally $instanceID;
then
  rallyFlag=0
else
  rallyFlag=1
fi

if [[ $rallyFlag -eq 0 ]] #is rallyServer
then
  rallyPrivateIP=$nodePrivateIP #This is the server that will create the cluster
else
  rallyInstanceID=$(getClusterInstance)
  rallyPrivateIP=$(aws ec2 describe-instances --region $region \
                 --query 'Reservations[*].Instances[*].NetworkInterfaces[0].PrivateIpAddress' \
                 --instance-ids $rallyInstanceID --output text)
fi

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'
echo services \'$services\'
echo stackName \'$stackName\'
echo rallyPrivateIP \'$rallyPrivateIP\'
echo region \'$region\'
echo instanceID \'$instanceID\'
echo nodePrivateIP \'$nodePrivateIP\'
echo rallyFlag \'$rallyFlag\'

#if [[ ${rallyPrivateIP} == ${nodePrivateIP} ]]
if [[ $rallyFlag -eq 0 ]] #true
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

  setCBClusterTag
fi

cd /opt/couchbase/bin/

echo "Running couchbase-cli node-init"
output=""
while [[ ! $output =~ "SUCCESS" ]]
do
  output=$(./couchbase-cli node-init \
    --cluster=$nodePrivateIP \
    --node-init-hostname=$nodePrivateIP \
    --node-init-data-path=/mnt/datadisk/data \
    --node-init-index-path=/mnt/datadisk/index \
    --user=$adminUsername \
    --pass=$adminPassword)
  echo node-init output \'$output\'
  sleep 10
done

if [[ $rallyFlag -eq 0 ]]
then
  totalRAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  dataRAM=$((50 * $totalRAM / 100000))
  indexRAM=$((25 * $totalRAM / 100000))

  echo "Running couchbase-cli cluster-init"
  ./couchbase-cli cluster-init \
    --cluster=$nodePrivateIP \
    --cluster-username=$adminUsername \
    --cluster-password=$adminPassword \
    --cluster-ramsize=$dataRAM \
    --cluster-index-ramsize=$indexRAM \
    --services=${services}

  setCBRallyTag
  setCBClusterTag
else
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "Server $nodePrivateIP:8091 added" && ! $output =~ 'Node is already part of cluster' ]]
  do
    output=$(./couchbase-cli server-add \
      --cluster=$rallyPrivateIP \
      --user=$adminUsername \
      --pass=$adminPassword \
      --server-add=$nodePrivateIP \
      --server-add-username=$adminUsername \
      --server-add-password=$adminPassword \
      --services=${services})
    echo server-add output \'$output\'
    sleep 10
  done

  echo "Running couchbase-cli rebalance"
  output=""
  while [[ ! $output =~ "SUCCESS" ]]
  do
    output=`./couchbase-cli rebalance \
    --cluster=$rallyPrivateIP \
    --user=$adminUsername \
    --pass=$adminPassword`
    echo rebalance output \'$output\'
    sleep 10
  done
  setCBClusterTag
fi


