#!/usr/bin/env bash

STACK_NAME=$1

TEMPLATE_BODY="file://couchbase-test.template"
REGION=`aws configure get region`

InstanceType="m5.xlarge"
ServerInstanceCount="2"
ServerDiskSize="100"
SyncGatewayInstanceCount="0"
SyncGatewayInstanceType="m5.large"
Username="couchbase"
Password="foo123!"
KeyName="couchbase-${REGION}"
#Uncomment below if you want to edit the services running on the nodes.  The data service is a minimum requirement
#Services"data,index,query,fts,eventing,analytics" 
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
#Uncomment below you uncommented Services in the variable definitions
#ParameterKey=KeyName,ParameterValue=${Services} \
ParameterKey=License,ParameterValue=${License}
