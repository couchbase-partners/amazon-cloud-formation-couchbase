#!/usr/bin/env bash

TEMPLATE_BODY="file://couchbase.template"
STACK_NAME=$1
REGION=`aws configure get region`

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

#echo "Validating template..."
#aws cloudformation validate-template --template-body ${TEMPLATE_BODY}

aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--template-body ${TEMPLATE_BODY} \
--stack-name ${STACK_NAME} \
--region ${REGION} \
--parameters \
ParameterKey=Username,ParameterValue=${USERNAME} \
ParameterKey=Password,ParameterValue=${PASSWORD} \
ParameterKey=KeyName,ParameterValue=${KEY_NAME}
