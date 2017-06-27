#!/usr/bin/env bash

TEMPLATE_BODY="file://couchbase.template"
STACK_NAME=$1
REGION=`aws configure get region`

ServerInstanceCount="4"
ServerDiskSize="100"
SyncGatewayInstanceCount="0"
INSTANCE_TYPE="m4.xlarge"
USERNAME="couchbase"
PASSWORD="foo123!"
KEY_NAME="couchbase-${REGION}"

KEY_FILENAME=~/.ssh/${KEY_NAME}.pem
if [ ! -e ${KEY_FILENAME} ]
then
  echo "The key does not exist.  Generating a new key."
  aws ec2 create-key-pair --region ${REGION} --key-name ${KEY_NAME} --query 'KeyMaterial' --output text > ${KEY_FILENAME}
  chmod 600 ${KEY_FILENAME}
  echo "Key saved to ${KEY_FILENAME}"
fi

aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--template-body ${TEMPLATE_BODY} \
--stack-name ${STACK_NAME} \
--region ${REGION} \
--parameters \
ParameterKey=ServerInstanceCount,ParameterValue=${ServerInstanceCount} \
ParameterKey=ServerDiskSize,ParameterValue=${ServerDiskSize} \
ParameterKey=SyncGatewayInstanceCount,ParameterValue=${SyncGatewayInstanceCount} \
ParameterKey=InstanceType,ParameterValue=${INSTANCE_TYPE} \
ParameterKey=Username,ParameterValue=${USERNAME} \
ParameterKey=Password,ParameterValue=${PASSWORD} \
ParameterKey=KeyName,ParameterValue=${KEY_NAME}
