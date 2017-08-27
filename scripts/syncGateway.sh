#!/usr/bin/env bash

echo "Running server.sh"

stackName=$1
rallyAutoScalingGroup=$2

echo "Using the settings:"
echo stackName \'$stackName\'
echo rallyAutoScalingGroup \'$rallyAutoScalingGroup\'

yum -y install jq
source util.sh

getRallyPublicDNS $stackName $rallyAutoScalingGroup
rallyPublicDNS=$?

./configureSyncGateway.sh $stackName $rallyPublicDNS
