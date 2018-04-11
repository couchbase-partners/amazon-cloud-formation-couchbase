#!/usr/bin/env bash

STACK_NAME=$1

TEMPLATE_BODY="file://byol.template"
REGION=`aws configure get region`

Username="couchbase"
Password="foo123!"
KeyName="couchbase-${REGION}"
SSHCIDR="0.0.0.0/0"

aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--template-body ${TEMPLATE_BODY} \
--stack-name ${STACK_NAME} \
--region ${REGION} \
--parameters \
ParameterKey=Username,ParameterValue=${Username} \
ParameterKey=Password,ParameterValue=${Password} \
ParameterKey=KeyName,ParameterValue=${KeyName} \
ParameterKey=SSHCIDR,ParameterValue=${SSHCIDR}
