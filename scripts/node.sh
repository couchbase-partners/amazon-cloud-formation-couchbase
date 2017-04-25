#!/usr/bin/env bash

echo "Running node.sh"

adminUsername=$1
adminPassword=$2

echo "Using the settings:"
echo adminUsername \'$adminUsername\'
echo adminPassword \'$adminPassword\'

./install.sh
./format.sh

# We seem to need a little time for the node to come up
sleep 10

./configure.sh $adminUsername $adminPassword
