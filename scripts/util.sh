#!/usr/bin/env bash

readonly CB_CLUSTER_TAG=cb:cluster-member
readonly CB_RALLY_TAG=cb:rally-server
readonly ERROR_RALLY_NOT_FOUND=55
readonly ERROR_CLUSTER_NOT_FOUND=56

getRegion ()
{
  local region=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/.$//')
  echo $region
}

getInstanceID ()
{
  local instanceID=$(curl http://169.254.169.254/latest/meta-data/instance-id)
  echo $instanceID
}

getStackName ()
{
  local region=$(getRegion)
  local instanceID=$(getInstanceID)
  local stackName=$(aws cloudformation describe-stack-resources --physical-resource-id $instanceID --query '(StackResources[*].StackName)[0]' --output text --region $region)
  echo $stackName
}

getStackID ()
{
  local region=$(getRegion)
  local instanceID=$(getInstanceID)
  local stackID=$(aws cloudformation describe-stack-resources --physical-resource-id $instanceID --query '(StackResources[*].StackId)[0]' --output text --region $region)
  echo $stackID
}

setCBClusterTag ()
{
  #TODO: handle exceptions more robustly - optional
  local region=$(getRegion)
  local instanceID=$(getInstanceID)
  local stackName=$(getStackName)
  aws ec2 create-tags --resources $instanceID --tags Key=$CB_CLUSTER_TAG,Value=$stackName --region $region
}

setCBRallyTag ()
{
  #TODO: handle exceptions more robustly - optional
  local region=$(getRegion)
  local instanceID=$(getInstanceID)
  local stackName=$(getStackName)
  aws ec2 create-tags --resources $instanceID --tags Key=$CB_RALLY_TAG,Value=$stackName --region $region
}

isRally ()
{
  # $1 = instanceID to compare with Rally's instanceID
  # TODO: handle arguments more robustly
  local instanceID=$1
  local region=$(getRegion)
  local stackName=$(getStackName)
  local rallyInstanceID=$(getRallyInstanceID)

  if [[ $instanceID == $rallyInstanceID ]]
  then
    echo "Rally found"
    return 0
  elif [[ $rallyInstanceID == $ERROR_RALLY_NOT_FOUND ]]
  then
    #TODO: handle this case where the rally check gave an error
    echo "Rally not found"
    return $ERROR_RALLY_NOT_FOUND
  else
    echo "Not the rally server"
    return 1
  fi
}

# Get the instance that is used to initialize the cluster.  This will instance will be required at the initial startup of the cluster/stack where
# potential members have to join a cluster or this instance has to return a cluster.
# it is jus the first instance returned from the query.
getRallyInstanceID ()
{
  local region=$(getRegion)
  local stackName=$(getStackName)

  count=1
  while [[ count -le 5 ]] 
  do
    #the rally server is just the first server in the reservation
    local rallyInstanceID=$(aws ec2 describe-instances --query '(Reservations[*].Instances[0].{ID:InstanceId})[0]' \
                  --filter "Name=tag-key,Values=aws:cloudformation:stack-name" "Name=tag-value,Values=$stackName" \
                  --region $region --output text)

    if [[ $rallyInstanceID == "None" ]]
    then
      count=$((count + 1))
      sleep 20
    else
      echo $rallyInstanceID
      return 0
    fi
  done
  echo $rallyInstanceID
  return $ERROR_RALLY_NOT_FOUND #TODO: handle error codes better.
}

getClusterInstance (){

  # First look for tagged resources with CB_CLUSTER_TAG 
  local region=$(getRegion)
  local stackName=$(getStackName)
  local cbInstanceID=$(aws ec2 describe-tags --query '(Tags[*].{id:ResourceId})[0]' \
             --filters "Name=tag:aws:cloudformation:stack-name,Values=$stackName,Name=tag:$CB_CLUSTER_TAG,Values=$stackName" \
             --region $region --output text)

  if [[ (! -z $cbInstanceID) && ($cbInstanceID != "None") ]] #found an eligible server
  then
    echo $cbInstanceID
    return 0
  else
    #Now check for a Rally server - A rallyServer would also have the tag, but potentially it hasn't set it yet, so we use this 
    #as a way to wait for it to be ready.  This happens in the the cluster-init stage

    cbInstanceID=$(getRallyInstanceID)
    if [ $? == $ERROR_RALLY_NOT_FOUND ] #need to wrap the error to distinguish the caller
    then
      echo $cbInstanceID
      return $ERROR_CLUSTER_NOT_FOUND
    else
      echo $cbInstanceID 
      return 0
    fi
  fi
}

formatDataDisk ()
{
  DEVICE=/dev/sdk
  MOUNTPOINT=/mnt/datadisk

  echo "Creating the filesystem."
  mkfs -t ext4 ${DEVICE}

  echo "Updating fstab"
  LINE="${DEVICE}\t${MOUNTPOINT}\text4\tdefaults,nofail\t0\t2"
  echo -e ${LINE} >> /etc/fstab

  echo "Mounting the disk"
  mkdir $MOUNTPOINT
  mount -a

  echo "Changing permissions"
  chown couchbase $MOUNTPOINT
  chgrp couchbase $MOUNTPOINT
}

getRallyPublicDNS ()
{
  region=$(getRegion)
 # region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
 #   | jq '.region'  \
 #   | sed 's/^"\(.*\)"$/\1/' )

  # if no rallyAutoscalingGroup was passed then the node this is running on is part of the rallyAutoscalingGroup
  if [ -z "$1" ]
  then
    instanceID=$(getInstanceID)
    #instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
    #  | jq '.instanceId' \
    #  | sed 's/^"\(.*\)"$/\1/' )

    rallyAutoScalingGroup=$(aws ec2 describe-instances \
      --region ${region} \
      --instance-ids ${instanceID})
     # \
     # | jq '.Reservations[0]|.Instances[0]|.Tags[] | select( .Key == "aws:autoscaling:groupName") | .Value' \
     # | sed 's/^"\(.*\)"$/\1/' )
  else
    rallyAutoScalingGroup=$1
  fi

  rallyAutoscalingGroupInstanceIDs=$(aws autoscaling describe-auto-scaling-groups \
    --region ${region} \
    --auto-scaling-group-name ${rallyAutoScalingGroup} \
    --query 'AutoScalingGroups[*].Instances[*].InstanceId' \
    | grep "i-" | sed 's/ //g' | sed 's/"//g' |sed 's/,//g' | sort)

  rallyInstanceID=`echo ${rallyAutoscalingGroupInstanceIDs} | cut -d " " -f1`

  # Check if any IDs are already the rally point and overwrite rallyInstanceID if so
  rallyAutoscalingGroupInstanceIDsArray=(`echo $rallyAutoscalingGroupInstanceIDs`)
  for instanceID in ${rallyAutoscalingGroupInstanceIDsArray[@]}; do
    tags=`aws ec2 describe-tags --region ${region}  --filter "Name=tag:Name,Values=*Rally" "Name=resource-id,Values=$instanceID"`
#    tags=`echo $tags # | jq '.Tags'`
    if [ "$tags" != "[]" ]
    then
      rallyInstanceID=$instanceID
    fi
  done

  rallyPublicDNS=$(aws ec2 describe-instances \
    --region ${region} \
    --query  'Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicDnsName' \
    --instance-ids ${rallyInstanceID} \
    --output text)

  echo ${rallyPublicDNS}
}

