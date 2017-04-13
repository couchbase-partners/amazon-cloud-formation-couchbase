#!/usr/bin/env bash

STACK_NAME=$1
aws cloudformation delete-stack --stack-name $STACK_NAME

