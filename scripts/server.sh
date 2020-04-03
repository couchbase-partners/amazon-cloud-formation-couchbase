#!/usr/bin/env bash
#TODO: remove or make tag false when terminating -- optional
#TODO: possibly do not need to pass the stackName
#TODO: think about the need to pass the autoscaling group
#TODO: Handle alternate address especially if the public IP is not available.  Right now only using private ips.
echo "Running server.sh"

adminUsername=$1
adminPassword=$2
services=$3
stackName=$4
version=$5

echo "Got the parameters:"
echo adminUsername \'"$adminUsername"\'
echo adminPassword \'"$adminPassword"\'
echo services \'"$services"\'
echo stackName \'"$stackName"\'
echo version \'"$version"\'

#######################################################"
############## Install Couchbase Server ###############"
#######################################################"
echo "Installing Couchbase Server..."

wget https://packages.couchbase.com/releases/"${version}"/couchbase-server-enterprise-"${version}"-amzn2.x86_64.rpm
rpm --install couchbase-server-enterprise-"${version}"-amzn2.x86_64.rpm

source util.sh

echo "Turning off transparent huge pages"
turnOffTransparentHugepages

echo "Setting swappiness to 0..."
setSwappinessToZero

echo "Formatting disk"
formatDataDisk
yum -y update
#yum -y install jq #TODO: May need jq later
#All servers that join the cluster successfully can allow others to be added the cluster using server-add.
#Initially there is one pre-defined rally server when the cluster is being initialized which is chosen based on the earliest LaunchTime node.

region=$(getRegion)
instanceID=$(getInstanceID)
nodePrivateDNS=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)
rallyPrivateDNS="$nodePrivateDNS" #Defaulting to this node but it will be overwritten (possibly with the same value) later 
nodePublicDNS=$(curl http://169.254.169.254/latest/meta-data/public-hostname) 
rallyPublicDNS="$nodePublicDNS" #Defaulting to this node but it will be overwritten (possibly with the same value) later
rallyInstanceID=$(getRallyInstanceID)
rallyFlag=$?
if [[ $rallyFlag ]] #exit 0 means it is the rally server (i.e. cluster initializing node)
then
  if [[ "$rallyInstanceID" == "$instanceID" ]] #If true this server is the cluster creator
  then
    rallyPrivateDNS="$nodePrivateDNS" 
    rallyPublicDNS="$nodePublicDNS"
  else
    DNSResult=$(getDNS "$rallyInstanceID") 
    DNSFlag=$?
    if [[ $?  ]]
    then
      read -a DNSarr <<< "$DNSResult"  # privateDNS [0] publicDNS [1]
    else
      echo "Can't continue because DNS can't be retrieved."
      exit 1
    fi
    rallyPrivateDNS=${DNSarr[0]}
    rallyPublicDNS=${DNSarr[1]}
  fi
else
  rallyInstanceID=$(getClusterInstance) #Any cluster with the $CB_RALLY_TAG tag
  DNSResult=$(getDNS "$rallyInstanceID") 
  DNSFlag=$?
  if [[ "$DNSFlag" ]]
  then
    read -a DNSarr <<< "$DNSResult"  # privateDNS [0] publicDNS [1]
  else
    echo "Can't continue because DNS can't be retrieved."
    exit 1
  fi
  rallyPrivateDNS=${DNSarr[0]}
  rallyPublicDNS=${DNSarr[1]} 
fi

echo "Using the settings:"
echo adminUsername \'"$adminUsername"\'
echo adminPassword \'"$adminPassword"\'
echo services \'"$services"\'
echo stackName \'"$stackName"\'
echo rallyPrivateDNS \'"$rallyPrivateDNS"\'
echo rallyPublicDNS \'"$rallyPublicDNS"\'
echo region \'"$region"\'
echo instanceID \'"$instanceID"\'
echo nodePublicDNS \'"$nodePublicDNS"\'
echo nodePrivateDNS \'"$nodePrivateDNS"\'
echo rallyFlag \'$rallyFlag\'
echo rallyInstanceID \'"$rallyInstanceID"\'

echo "Switching to couchbase installation directory"
cd /opt/couchbase/bin/ || exit

echo "Running couchbase-cli node-init"
output=""
# --node-init-hostname=$rallyPrivateDNS \ TODO: May not be needed retun to the node-init line if needed
while [[ ! $output =~ "SUCCESS" ]]
do
  #TODO: Handle different services and their folders based on the running services
  output=$(./couchbase-cli node-init \
    --cluster="$rallyPrivateDNS" \
    --node-init-data-path=/mnt/datadisk/data \
    --node-init-index-path=/mnt/datadisk/index \
    -u="$adminUsername" \
    -p="$adminPassword")
  echo node-init output \'"$output"\'
  sleep 10
done

if [[ $rallyFlag ]] #Rally
then
  echo "Creating node tag for Rally (cluster initialization) Node Name"
  aws ec2 create-tags \
  --region "${region}" \
  --resources "${rallyInstanceID}" \
  --tags Key=Name,Value="${stackName}"-ServerRally

  totalRAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  dataRAM=(40 * "$totalRAM" / 100000)
  indexRAM=(8 * "$totalRAM" / 100000)

  #--index-storage-setting=memopt \ TODO: may not need to set memopt
  echo "Running couchbase-cli cluster-init"
  ./couchbase-cli cluster-init \
    --cluster="$rallyPrivateDNS" \
    --cluster-username="$adminUsername" \
    --cluster-password="$adminPassword" \
    --cluster-ramsize=$dataRAM \
    --cluster-index-ramsize=$indexRAM \
    --cluster-analytics-ramsize=$indexRAM \
    --cluster-fts-ramsize=$indexRAM \
    --cluster-eventing-ramsize=$indexRAM \
    --services="${services}"

  setCBRallyTag
  setCBClusterTag
else
  echo "Creating node tag for Node Name"
  aws ec2 create-tags \
    --region "${region}" \
    --resources "${instanceID}" \
    --tags Key=Name,Value="${stackName}"-Server
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "Server $nodePrivateDNS:8091 added" && ! $output =~ 'Node is already part of cluster' ]]
  do
    output=$(./couchbase-cli server-add \
      --cluster="$rallyPrivateDNS" \
      -u="$adminUsername" \
      -p="$adminPassword" \
      --server-add="$nodePrivateDNS" \
      --server-add-username="$adminUsername" \
      --server-add-password="$adminPassword" \
      --services="${services}")
    echo server-add output \'"$output"\'
    sleep 10
  done

  echo "Running couchbase-cli rebalance"
  output=""
  while [[ ! $output =~ "SUCCESS" ]]
  do
    output=$(./couchbase-cli rebalance \
    --cluster="$rallyPrivateDNS" \
    -u="$adminUsername" \
    -p="$adminPassword")
    echo rebalance output \'"$output"\'
    sleep 10
  done
  setCBClusterTag
fi


