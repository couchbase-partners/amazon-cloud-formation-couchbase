#!/usr/bin/env bash

STACK_NAME=$1

TEMPLATE_BODY="file://couchbase-ee.template"
REGION=`aws configure get region`

ServerInstanceCount="4"
ServerDiskSize="100"
SyncGatewayInstanceCount="2"
InstanceType="m4.xlarge"
Username="couchbase"
Password="foo123!"
KeyName="couchbase-${REGION}"
License="BYOL"

aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--template-body ${TEMPLATE_BODY} \
--stack-name ${STACK_NAME} \
--region ${REGION} \
--parameters \
ParameterKey=ServerInstanceCount,ParameterValue=${ServerInstanceCount} \
ParameterKey=ServerDiskSize,ParameterValue=${ServerDiskSize} \
ParameterKey=SyncGatewayInstanceCount,ParameterValue=${SyncGatewayInstanceCount} \
ParameterKey=InstanceType,ParameterValue=${InstanceType} \
ParameterKey=Username,ParameterValue=${Username} \
ParameterKey=Password,ParameterValue=${Password} \
ParameterKey=KeyName,ParameterValue=${KeyName} \
ParameterKey=License,ParameterValue=${License}
