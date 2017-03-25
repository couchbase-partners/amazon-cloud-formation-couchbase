#!/bin/sh

TEMPLATE_BODY=`cat ./cloud-formation-couchbase.json`
STACK_NAME=$1
REGION=`aws configure get region`

KEYNAME=""
COUCHBASE_USERNAME="couchbase"
COUCHBASE_PASSWORD="foo123!"

aws cloudformation validate-template --template-body $TEMPLATE_BODY

aws cloudformation create-stack \
--template-body $TEMPLATE_BODY \
--stack-name $STACK_NAME \
--region $REGION \
--parameters \
ParameterKey=KeyName,ParameterValue=$KEYNAME \
ParameterKey=Admin,ParameterValue=$COUCHBASE_USERNAME \
ParameterKey=Password,ParameterValue=$COUCHBASE_PASSWORD \
