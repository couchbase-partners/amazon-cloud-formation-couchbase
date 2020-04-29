#!/usr/bin/env bash

#This is on the 
STACK_NAME=$1


TEMPLATE_BODY="file://couchbase-ee-PO-AG-6-plus.template"
REGION=`aws configure get region`

InstanceType="r5.xlarge"
ServerInstanceCount="3"
ServerDiskSize="100"
SyncGatewayInstanceCount="0"
SyncGatewayInstanceType="m5.large"
Username="couchbase"
Password="foo123!"
KeyName="couchbase-${REGION}" #The ssh key that will be used to connect to the nodes
#Uncomment the line below if you want to edit the services running on the nodes.  The data service is a minimum requirement
#Services"data,index,query,fts,eventing,analytics" 
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
#ParameterKey=KeyName,ParameterValue=${Services} \
ParameterKey=ServerLicense,ParameterValue=${ServerLicense}
ParameterKey=SGWLicense,ParameterValue=${SGWLicense}
