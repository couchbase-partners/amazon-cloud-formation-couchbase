#!/bin/sh

PARAMETERS_FILE=$1
STACK_NAME=$2

# create generatedTemplate.json
python generator_beta.py parameters/${PARAMETERS_FILE}.yaml

 TEMPLATE_BODY="file://generated_beta.template"
 REGION=`aws configure get region`

 Username="couchbase"
 Password="foo123!"
 KeyName="couchbase-${REGION}"
 License="BYOL"

 aws cloudformation create-stack \
 --capabilities CAPABILITY_IAM \
 --template-body ${TEMPLATE_BODY} \
 --stack-name ${STACK_NAME} \
 --region ${REGION} \
 --parameters \
 ParameterKey=Username,ParameterValue=${Username} \
 ParameterKey=Password,ParameterValue=${Password} \
 ParameterKey=KeyName,ParameterValue=${KeyName}
