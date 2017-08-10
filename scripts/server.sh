#!/usr/bin/env bash

echo "Running server.sh"

serverAutoScalingGroup=$1
adminUsername=$2
adminPassword=$3

echo "Using the settings:"
echo serverAutoScalingGroup \'$serverAutoScalingGroup\'
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'

./configureOS.sh
./format.sh
./configureServer.sh $serverAutoScalingGroup $adminUsername $adminPassword
