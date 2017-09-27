#!/usr/bin/env bash

STACK_NAME=$1

LICENSE="hourly-pricing"
TEMPLATE_BODY="file://couchbase-server-ee-${LICENSE}.template"
REGION=`aws configure get region`

ServerInstanceCount="4"
ServerDiskSize="100"
InstanceType="m4.xlarge"
Username="couchbase"
Password="foo123!"
KeyName="couchbase-${REGION}"

aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--template-body ${TEMPLATE_BODY} \
--stack-name ${STACK_NAME} \
--region ${REGION} \
--parameters \
ParameterKey=ServerInstanceCount,ParameterValue=${ServerInstanceCount} \
ParameterKey=ServerDiskSize,ParameterValue=${ServerDiskSize} \
ParameterKey=InstanceType,ParameterValue=${InstanceType} \
ParameterKey=Username,ParameterValue=${Username} \
ParameterKey=Password,ParameterValue=${Password} \
ParameterKey=KeyName,ParameterValue=${KeyName} \
ParameterKey=SSHCIDR,ParameterValue="0.0.0.0/0"
