#!/usr/bin/env bash

echo "Running server.sh"

serverAutoScalingGroup=$1
stackName=$2

echo "Using the settings:"
echo serverAutoScalingGroup \'$serverAutoScalingGroup\'
echo stackName \'$stackName\'

yum -y install jq
./configureSyncGateway.sh $serverAutoScalingGroup $stackName
