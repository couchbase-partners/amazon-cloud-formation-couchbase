#!/usr/bin/env bash

getRallyPublicDNS ()
{
  region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
    | jq '.region'  \
    | sed 's/^"\(.*\)"$/\1/' )

  # if no rallyAutoscalingGroup was passed then the node this is running on is part of the rallyAutoscalingGroup
  if [ -z "$1" ]
  then
    instanceID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document \
      | jq '.instanceId' \
      | sed 's/^"\(.*\)"$/\1/' )

    rallyAutoScalingGroup=$(aws ec2 describe-instances \
      --region ${region} \
      --instance-ids ${instanceID} \
      | jq '.Reservations[0]|.Instances[0]|.Tags[] | select( .Key == "aws:autoscaling:groupName") | .Value' \
      | sed 's/^"\(.*\)"$/\1/' )
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
    tags=`echo $tags | jq '.Tags'`
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
