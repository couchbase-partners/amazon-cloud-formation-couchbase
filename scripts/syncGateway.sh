#!/usr/bin/env bash

echo "Running server.sh"

stackName=$1
rallyAutoScalingGroup=$2

echo "Using the settings:"
echo stackName \'$stackName\'
echo rallyAutoScalingGroup \'$rallyAutoScalingGroup\'

yum -y install jq
#### need to set rallyPublicDNS
./configureSyncGateway.sh $stackName $rallyPublicDNS
