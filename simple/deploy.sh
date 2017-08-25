#!/usr/bin/env bash

STACK_NAME=$1

LICENSE=hourly-pricing
TEMPLATE_BODY="file://couchbase-ee-${LICENSE}.template"
REGION=`aws configure get region`

ServerInstanceCount="4"
ServerDiskSize="100"
SyncGatewayInstanceCount="2"
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
