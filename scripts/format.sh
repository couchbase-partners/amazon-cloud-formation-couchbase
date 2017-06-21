#!/usr/bin/env bash

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
