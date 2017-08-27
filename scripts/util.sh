#!/usr/bin/env bash

getRallyPublicDNS ()
{
  stackName=$1

  region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
    | jq '.region'  \
    | sed 's/^"\(.*\)"$/\1/' )

  # if no rallyAutoscalingGroup was passed then the node this is running on is part of the rallyAutoscalingGroup
  if [ -z "$2" ]
  then
    instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
      | jq '.instanceId' \
      | sed 's/^"\(.*\)"$/\1/' )

      rallyAutoscalingGroup=$(aws ec2 describe-instances \
        --region ${region} \
        --instance-ids ${instanceID} \
        | jq '.Reservations[0]|.Instances[0]|.Tags[] | select( .Key == "aws:autoscaling:groupName") | .Value' \
        | sed 's/^"\(.*\)"$/\1/' )
  else
    rallyAutoScalingGroup=$2
  fi

  rallyAutoscalingGroupInstanceIDs=$(aws autoscaling describe-auto-scaling-groups \
    --region ${region} \
    --auto-scaling-group-name ${rallyAutoscalingGroup} \
    --query 'AutoScalingGroups[*].Instances[*].InstanceId' \
    | grep "i-" | sed 's/ //g' | sed 's/"//g' |sed 's/,//g' | sort)

  rallyInstanceID=`echo ${rallyAutoscalingGroupInstanceIDs} | cut -d " " -f1`

  rallyPublicDNS=$(aws ec2 describe-instances \
    --region ${region} \
    --query  'Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicDnsName' \
    --instance-ids ${rallyInstanceID} \
    --output text)

  return ${rallyPublicDNS}
}
