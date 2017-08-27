#!/usr/bin/env bash

echo "Running server.sh"

adminUsername=$1
adminPassword=$2
services=$3
stackName=$4

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'
echo services \'$services\'
echo stackName \'$stackName\'

yum -y update
yum -y install jq
source util.sh

formatDataDisk
turnOffTransparentHugepages
setSwappinessToZero

# if no rallyAutoscalingGroup was passed then the node this is running on is part of the rallyAutoscalingGroup
if [ -z "$4" ]
then
  rallyPublicDNS=`getRallyPublicDNS $stackName`
else
  rallyAutoScalingGroup=$4
  rallyPublicDNS=`getRallyPublicDNS $stackName $rallyAutoScalingGroup`
fi

./configureServer.sh $stackName $rallyPublicDNS $adminUsername $adminPassword $services
