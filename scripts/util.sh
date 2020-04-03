#!/usr/bin/env bash

readonly LOOP_COUNT_CREATOR=5
readonly CB_CLUSTER_TAG=cb:server:cluster-member
readonly CB_RALLY_TAG=cb:server:rally-node
readonly ERROR_RALLY_NOT_FOUND=55
readonly ERROR_CLUSTER_CREATOR_NOT_FOUND=56
readonly ERROR_PRIVATE_IP_NOT_FOUND=57
readonly ERROR_PUBLIC_IP_NOT_FOUND=58
readonly ERROR_DNS_NOT_FOUND=59
readonly GENERAL_SLEEP_TIMEOUT=60

#TODO: Set common variables like region, instanceId and stack name at start and only once.
getRegion ()
{
  local region=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/.$//')
  echo $region
}

getInstanceId ()
{
  local instanceId=$(curl http://169.254.169.254/latest/meta-data/instance-id)
  echo $instanceId
}

getStackName ()
{
  local region=$(getRegion)
  local instanceId=$(getInstanceId)
  local stackName=$(aws cloudformation describe-stack-resources --physical-resource-id $instanceId \
        --query 'StackResources[0].StackName' --output text --region $region)
  echo $stackName
}

getStackID ()
{
  local region=$(getRegion)
  local instanceId=$(getInstanceId)
  local stackID=$(aws cloudformation describe-stack-resources --physical-resource-id $instanceId --query 'StackResources[0].StackId' --output text --region $region)
  echo "$stackID"
}

setCBClusterTag ()
{
  #TODO: handle exceptions more robustly - optional
  local region=$(getRegion)
  local instanceId=$(getInstanceId)
  local stackName=$(getStackName)
  aws ec2 create-tags --resources "$instanceId" --tags Key=$CB_CLUSTER_TAG,Value=$stackName --region $region
}

setCBRallyTag ()
{
  #TODO: handle exceptions more robustly - optional
  local region=$(getRegion)
  local instanceId=$(getInstanceId)
  local stackName=$(getStackName)
  aws ec2 create-tags --resources $instanceId --tags Key=$CB_RALLY_TAG,Value=$stackName --region $region
}

isClusterCreator ()
{
  # $1 = instanceId to compare with Rally's instanceId
  # TODO: handle arguments more robustly
  local instanceId=$1
  local region=$(getRegion)
  local stackName=$(getStackName)
  local rallyInstanceId=$(getRallyInstanceId)
  local getRallyReturnCode="$?"
  
  if [[ $getRallyReturnCode -eq 0 ]]
  then
    if [[ $instanceId == "$rallyInstanceId" ]]
    then
      echo "Creator node found"
      return 0
    elif [[ $rallyInstanceId == $ERROR_RALLY_NOT_FOUND ]]
    then
      #TODO: handle this case where the rally check gave an error
      echo "Creator node not found"
      return $ERROR_CLUSTER_CREATOR_NOT_FOUND
    else
      echo "Not the rally server"
      return 1
    fi
  fi
}

#$1 - Optional instanceid if not provided use the instanceId of this node
getPublicIp ()
{
  local region=$(getRegion)
  local stackName=$(getStackName)
  if [ -z "$1" ]; then
    local instanceId=$(getInstanceId)
  else
    local instanceId="$1"
  fi
  local count=1 
  #There is an edge case when the server in question may be terminated right when this is called.  
  #This may lead to a problem since the instance Id may change when it restarted.
  #TODO: handle the above edge case that may be from the caller
  while [[ count -le $LOOP_COUNT_CREATOR ]] 
  do
    local publicIp=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].PublicIpAddress' \
          --filters "Name=instance-id,Values=$instanceId" "Name=instance-state-name,Values=running" --region "$region" --output text)
    if [[ -z "$publicIp" ]] || [[ "$publicIp" == "None" ]]
    then
      ((++count))
      sleep $GENERAL_SLEEP_TIMEOUT 
    else
      echo $publicIp
      return 0
    fi
  done
  echo "No Private IP was found - recheck the instance id."
  return $ERROR_PUBLIC_IP_NOT_FOUND 
}

#$1 - Optional instanceid if not provided use the instanceId of this node
#returns a string in the form (privateDNS[:space]publicDNS)
getDNS ()
{
  local region=$(getRegion)
  local stackName=$(getStackName)
  if [ -z "$1" ]; then
    local instanceId=$(getInstanceId)
  else
    local instanceId="$1"
  fi
  local count=1 
  #There is an edge case when the server in question may be terminated right when this is called.  
  #This may lead to a problem since the InstanceId may change when it restarted.
  #TODO: handle the above edge case that may be from the caller
  while [[ count -le $LOOP_COUNT_CREATOR ]] 
  do
    local DNS=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[PrivateDnsName,PublicDnsName]' --filters "Name=instance-id,Values=$instanceId" "Name=instance-state-name,Values=running" --region $region --output text)
    if [[ -z "$DNS" ]] || [[ "$DNS" == "None" ]] || [[ "$DNS" =~ "Could" ]]
    then
      ((++count))
      sleep $GENERAL_SLEEP_TIMEOUT 
    else
      echo $DNS
      return 0
    fi
  done
  echo "Could not get the DNS values"
  return $ERROR_DNS_NOT_FOUND 
}

getPrivateIp ()
{
  local region=$(getRegion)
  local stackName=$(getStackName)
  if [ -z "$1" ]; then
    local instanceId=$(getInstanceId)
  else
    local instanceId="$1"
  fi
  local count=1 
  #There is an edge case when the server in question may be terminated right when this is called.  
  #This may lead to a problem since the InstanceId may change when it restarted.
  #TODO: handle the above edge case that may be from the caller
  while [[ count -le $LOOP_COUNT_CREATOR ]] 
  do
    local privateIp=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].PrivateIpAddress' --filters "Name=instance-id,Values=$instanceId" "Name=instance-state-name,Values=running" --region $region --output text)
    if [[ -z "$privateIp" ]] || [[ "$privateIp" == "None" ]]
    then
      ((++count))
      sleep $GENERAL_SLEEP_TIMEOUT 
    else
      echo "$privateIp"
      return 0
    fi
  done
  echo "No Private IP was found - recheck the instance id."
  return $ERROR_PRIVATE_IP_NOT_FOUND 
}

# Get the instance that is used to initialize the cluster.  This instance will be required at the initial startup of the cluster/stack where
# potential members have to join a cluster. It is the first instance to be created based on the LaunchTime. 
getRallyInstanceId ()
{
  local region=$(getRegion)
  local stackName=$(getStackName)
  local count=1
  while [[ count -le $LOOP_COUNT_CREATOR ]] 
  do
    #Return the LaunchTime of the Rally Instance by sorting
    local rallyLaunchTime=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].LaunchTime' \
          --filters "Name=tag:aws:cloudformation:stack-name,Values=$stackName" "Name=instance-state-name,Values=running" \
          --region "$region" --output text | tr '\t' '\n' | sort -n | head -1)
    #Now use that LaunchTime to get the InstanceId
    local rallyInstanceId=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' \
          --filters "Name=tag:aws:cloudformation:stack-name,Values=$stackName" "Name=launch-time,Values=$rallyLaunchTime" \
          "Name=instance-state-name,Values=running" --region $region --output text)
    if [[ -z $rallyInstanceId ]] || [[ $rallyInstanceId == "None" ]]
    then
      ((++count))
      sleep $GENERAL_SLEEP_TIMEOUT 
    else
      echo $rallyInstanceId
      return 0
    fi
  done
  echo "The Rally was not found before the timeout period, Check that at least one Couchbase Server node has successfully launched."
  return $ERROR_RALLY_NOT_FOUND 
}

getClusterInstance (){

  # First look for tagged resources with $CB_CLUSTER_TAG 
  local region=$(getRegion)
  local stackName=$(getStackName)
  local count=1           
  while
   [[ -z $cbInstanceID && count -le $LOOP_COUNT_CREATOR ]] 
  do
    local cbInstanceID=$(aws ec2 describe-instances --query '(Reservations[*].Instances[*].InstanceId)[0]' \
          --filters "Name=tag:aws:cloudformation:stack-name,Values=$stackName" \
          "Name=instance-state-name,Values=running,Name=tag-key,Values=$CB_CLUSTER_TAG" --region $region --output text)
    if [[ $cbInstanceID == "None" ]]
    then
      ((++count))
      sleep $GENERAL_SLEEP_TIMEOUT 
    else
      echo $cbInstanceID
      return 0
    fi
  done
  echo "A Couchbase Server Cluster member was not found before the timeout period, Check that at least one Couchbase Server node has successfully joined the cluster." 
  return $ERROR_RALLY_NOT_FOUND
}

formatDataDisk ()
{
  DEVICE=/dev/sdk
  MOUNTPOINT=/mnt/datadisk

  echo "Creating the filesystem."
  mkfs -t ext4 ${DEVICE} #TODO: change to xfs and other settings

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
    instanceId=$(getInstanceId)
    #instanceId=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
    #  | jq '.instanceId' \
    #  | sed 's/^"\(.*\)"$/\1/' )

    rallyAutoScalingGroup=$(aws ec2 describe-instances \
      --region "$region" \
      --instance-ids "$instanceId")
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

  rallyInstanceId=$(echo ${rallyAutoscalingGroupInstanceIDs} | cut -d " " -f1)

  # Check if any IDs are already the rally point and overwrite rallyInstanceId if so
  rallyAutoscalingGroupInstanceIDsArray=$(echo $rallyAutoscalingGroupInstanceIDs)
  for instanceId in "${rallyAutoscalingGroupInstanceIDsArray[@]}"; do
    tags=$(aws ec2 describe-tags --region "$region"  --filter "Name=tag:Name,Values=*Rally" "Name=resource-id,Values="$instanceId"")
#    tags=`echo $tags # | jq '.Tags'`
    if [ "$tags" != "[]" ]
    then
      rallyInstanceId=$instanceId
    fi
  done

  rallyPublicDNS=$(aws ec2 describe-instances \
    --region ${region} \
    --query  'Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicDnsName' \
    --instance-ids ${rallyInstanceId} \
    --output text)

  echo ${rallyPublicDNS}
}

turnOffTransparentHugepages ()
{
  echo "#!/bin/bash
  ### BEGIN INIT INFO
  # Provides:          disable-thp
  # Required-Start:    $local_fs
  # Required-Stop:
  # X-Start-Before:    couchbase-server
  # Default-Start:     2 3 4 5
  # Default-Stop:      0 1 6
  # Short-Description: Disable THP
  # Description:       disables Transparent Huge Pages (THP) on boot
  ### END INIT INFO
  echo 'never' > /sys/kernel/mm/transparent_hugepage/enabled
  echo 'never' > /sys/kernel/mm/transparent_hugepage/defrag
  " > /etc/init.d/disable-thp
  chmod 755 /etc/init.d/disable-thp
  service disable-thp start
  chkconfig disable-thp on
}

setSwappinessToZero ()
{
  sysctl vm.swappiness=0
  echo "
  # Required for Couchbase
  vm.swappiness = 0
  " >> /etc/sysctl.conf
}