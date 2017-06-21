#!/usr/bin/env bash

echo "Running server.sh"

adminUsername=$1
adminPassword=$2

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'

./format.sh
./installServer.sh
./configureServer.sh $adminUsername $adminPassword
