#!/usr/bin/env bash

echo "Running server.sh"

stackName=$1
rallyAutoScalingGroup=$2

echo "Using the settings:"
echo stackName \'$stackName\'
echo rallyAutoScalingGroup \'$rallyAutoScalingGroup\'

yum -y update
yum -y install jq
source util.sh
rallyPublicDNS=`getRallyPublicDNS $stackName $rallyAutoScalingGroup`
./configureSyncGateway.sh $stackName $rallyPublicDNS
