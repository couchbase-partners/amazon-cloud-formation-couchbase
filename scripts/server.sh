#!/usr/bin/env bash

echo "Running server.sh"

adminUsername=$1
adminPassword=$2
stackName=$3

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'
echo stackName \'$stackName\'

./configureOS.sh
./format.sh
./configureServer.sh $adminUsername $adminPassword $stackName
