#!/usr/bin/env bash

#Use only if you have a private offer with Couchbase for Couchbase Server and Sync Gateway Linux 2

STACK_NAME=$1


TEMPLATE_BODY="file://couchbase-ee-private-offer-annual1-6-plus.template"
REGION=`aws configure get region`

#Universal Settings
Username="couchbase" #For the Couchbase Web Console
Password="foo123!" #For the Couchbase Web Console
KeyName="couchbase-${REGION}" #The ssh key that will be used to connect to the nodes

#Couchbase Server Settings
InstanceType="m5.xlarge" #Couchbase Server Instance Type
ServerInstanceCount="3"
ServerDiskSize="100"
ServerVersion="6.5.0"
Services="data" #seperate each service with \\, e.g data\\,index\\,query\\,fts\\,eventing\\,analytics
ServerLicense=HourlyPricing #Couchbase Server license use: ANNUAL or HourlyPricing

#Couchbase Sync Gateway Settings
SyncGatewayVersion="2.7.1"
SyncGatewayInstanceCount="0"
SyncGatewayInstanceType="m5.large"
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
ParameterKey=Services,ParameterValue=${Services} \
ParameterKey=ServerVersion,ParameterValue=${ServerVersion} \
ParameterKey=SyncGatewayVersion,ParameterValue=${SyncGatewayVersion} \
ParameterKey=ServerLicense,ParameterValue=${ServerLicense} \
ParameterKey=SGWLicense,ParameterValue=${SGWLicense} # --generate-cli-skeleton 
