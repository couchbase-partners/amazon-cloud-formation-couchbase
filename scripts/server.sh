#!/usr/bin/env bash

echo "Running server.sh"

adminUsername=$1
adminPassword=$2

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'

./installServer.sh
./format.sh
./configureServer.sh $adminUsername $adminPassword
