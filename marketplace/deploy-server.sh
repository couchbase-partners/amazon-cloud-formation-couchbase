#!/usr/bin/env bash

STACK_NAME=$1

LICENSE="byol"
TEMPLATE_BODY="file://couchbase-server-ee-${LICENSE}.template"
REGION=`aws configure get region`

InstanceCount="4"
DiskSize="100"
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
ParameterKey=InstanceCount,ParameterValue=${InstanceCount} \
ParameterKey=DiskSize,ParameterValue=${DiskSize} \
ParameterKey=InstanceType,ParameterValue=${InstanceType} \
ParameterKey=Username,ParameterValue=${Username} \
ParameterKey=Password,ParameterValue=${Password} \
ParameterKey=KeyName,ParameterValue=${KeyName} \
ParameterKey=SSHCIDR,ParameterValue="0.0.0.0/0"
