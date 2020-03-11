#!/usr/bin/env bash

STACK_NAME=$1

TEMPLATE_BODY="file://couchbase-ee.60plus.template"
REGION=`aws configure get region`

InstanceType="m5.xlarge"
ServerInstanceCount="1"
ServerDiskSize="100"
SyncGatewayInstanceCount="1"
SyncGatewayInstanceType="m5.large"
Username="couchbase"
Password="foo123!"
KeyName="couchbase-${REGION}"
License=HourlyPricing #BYOL or HourlyPricing


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
