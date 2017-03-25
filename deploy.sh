#!/bin/sh

TEMPLATE_BODY="file://cloud-formation-couchbase.json"
STACK_NAME=$1
REGION=`aws configure get region`

COUCHBASE_USERNAME="couchbase"
COUCHBASE_PASSWORD="foo1234"
KEY="couchbase-$REGION"

echo "Getting SSH key..."
KEY_FILENAME="~/.ssh/$KEY.pem"
if [ ! -e $KEY_FILENAME ]
then
  echo "The key does not exist.  Generating a new key."
  aws ec2 create-key-pair --region $REGION --key-name $KEY --query 'KeyMaterial' --output text > $KEY_FILENAME
  chmod 600 $KEY_FILENAME
  echo "Key saved to $KEY_FILENAME"
fi

echo "Validating template..."
aws cloudformation validate-template --template-body $TEMPLATE_BODY 1>/dev/null

aws cloudformation create-stack \
--template-body $TEMPLATE_BODY \
--stack-name $STACK_NAME \
--region $REGION \
--parameters \
ParameterKey=Admin,ParameterValue=$COUCHBASE_USERNAME \
ParameterKey=Password,ParameterValue=$COUCHBASE_PASSWORD \
ParameterKey=KeyName,ParameterValue=$KEY
