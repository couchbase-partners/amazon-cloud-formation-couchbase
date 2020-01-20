#!/usr/bin/env bash

STACK_NAME=$1

TEMPLATE_BODY="file://couchbase-ee.template"
REGION=`aws configure get region`

ServerInstanceCount="3"
ServerDiskSize="100"
SyncGatewayInstanceCount="1"
InstanceType="m5.xlarge"
Username="couchbase"
Password="foo123!"
KeyName="couchbase-${REGION}"
License=BYOL #BYOL or HourlyPricing
LicenseSelect=BYOL #BYOL or HourlyPricing for lower than server 6.0.0.  For greater than 6.0.0 or to use Amazon Linux 2 BYOL6 or HourlyPricing6


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
ParameterKey=License,ParameterValue=${LicenseSelect}
