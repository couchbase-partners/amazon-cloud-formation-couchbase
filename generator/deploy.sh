#!/bin/sh

PARAMETERS_FILE=$1
STACK_NAME=$2

# create generatedTemplate.json
python deployment.py parameters.${PARAMETERS_FILE}.yaml

TEMPLATE_BODY="file://generated.template"
REGION=`aws configure get region`

USERNAME="couchbase"
PASSWORD="foo123!"
KEY_NAME="couchbase-${REGION}"

aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--template-body ${TEMPLATE_BODY} \
--stack-name ${STACK_NAME} \
--region ${REGION} \
--parameters \
ParameterKey=Username,ParameterValue=${USERNAME} \
ParameterKey=Password,ParameterValue=${PASSWORD} \
ParameterKey=KeyName,ParameterValue=${KEY_NAME}
