#!/usr/bin/env bash

#Use only if you have a private offer with Couchbase for Couchbase Server and Sync Gateway Linux 2
#If you do not this will not work for you

STACK_NAME=$1


TEMPLATE_BODY="file://couchbase-ee-private-offer-annual1-6-plus.template"
REGION=`aws configure get region`

InstanceType="r5.xlarge" #Couchbase Server Instace Type
ServerInstanceCount="3"
ServerDiskSize="100"
SyncGatewayInstanceCount="0"
SyncGatewayInstanceType="m5.large"
Username="couchbase" #For the Couchbase Web Console
Password="foo123!" #For the Couchbase Web Console
KeyName="couchbase-${REGION}" #The ssh key that will be used to connect to the nodes
Services="data,index" 
ServerLicense=HourlyPricing #Couchbase Server license use: ANNUAL or HourlyPricing
SGWLicense=BYOL #Couchbase Sync Gateway license use: BYOL or HourlyPricing

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
ParameterKey=Services,ParameterValue=${Services} \
ParameterKey=ServerLicense,ParameterValue=${ServerLicense}
ParameterKey=SGWLicense,ParameterValue=${SGWLicense}
