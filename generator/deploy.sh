#!/bin/sh

PARAMETERS_FILE=$1
STACK_SET=$2

# create generatedTemplate.json
python deployment.py parameters.${PARAMETERS_FILE}.yaml

# need to create the stack set
# ...
