#!/usr/bin/env bash

STACK_NAME=$1

TEMPLATE_BODY="file://261a9b6d-4be2-40b3-bb5f-80930a4a9570.458010ec-a1ef-41de-b2bc-377eaf74f1c5.template"
REGION=`aws configure get region`

ServerInstanceCount="4"
ServerDiskSize="100"
SyncGatewayInstanceCount="2"
InstanceType="m4.xlarge"
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
ParameterKey=ServerInstanceCount,ParameterValue=${ServerInstanceCount} \
ParameterKey=ServerDiskSize,ParameterValue=${ServerDiskSize} \
ParameterKey=SyncGatewayInstanceCount,ParameterValue=${SyncGatewayInstanceCount} \
ParameterKey=InstanceType,ParameterValue=${InstanceType} \
ParameterKey=Username,ParameterValue=${Username} \
ParameterKey=Password,ParameterValue=${Password} \
ParameterKey=KeyName,ParameterValue=${KeyName} \
ParameterKey=SSHCIDR,ParameterValue=${SSHCIDR}
