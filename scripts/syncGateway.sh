#!/usr/bin/env bash

echo "Running server.sh"

serverAutoScalingGroup=$1

echo "Using the settings:"
echo serverAutoScalingGroup \'$serverAutoScalingGroup\'

./configureSyncGateway.sh $serverAutoScalingGroup
