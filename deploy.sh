#!/bin/sh

TEMPLATE_BODY="file://cloud-formation-couchbase.json"
STACK_NAME=$1
REGION=`aws configure get region`

COUCHBASE_USERNAME="couchbase"
COUCHBASE_PASSWORD="foo1234"

echo "Getting keypair..."
if [ -e ~/.ssh/couchbase-keypair-$REGION.pem ] && [ -z "$KEY" ]
then
  echo "Default key exists"
  KEY=couchbase-keypair-$REGION
elif [ -z "$KEY" ]
then
  echo "No key-pair passed, generating key-pair..."
  aws ec2 create-key-pair --region $REGION --key-name couchbase-keypair-$REGION --query 'KeyMaterial' --output text > ~/.ssh/couchbase-keypair-$REGION.pem
  if [ $? -gt 0 ]
  then
    echo "Key generation error. Exiting..."
    exit(1)
  fi
  chmod 600 ~/.ssh/couchbase-keypair-$REGION.pem
  KEY=couchbase-keypair-$REGION
  echo "Key saved to ~/.ssh/$KEY.pem"
fi

echo "Validating template..."
aws cloudformation validate-template --template-body $TEMPLATE_BODY 1>/dev/null
if [ $? -gt 0 ]
then
  echo "Template validation error. Exiting..."
  exit(1)
fi

aws cloudformation create-stack \
--template-body $TEMPLATE_BODY \
--stack-name $STACK_NAME \
--region $REGION \
--parameters \
ParameterKey=Admin,ParameterValue=$COUCHBASE_USERNAME \
ParameterKey=Password,ParameterValue=$COUCHBASE_PASSWORD \
ParameterKey=KeyName,ParameterValue=$KEY
