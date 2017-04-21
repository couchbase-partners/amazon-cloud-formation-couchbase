#!/usr/bin/env bash

DISK="/dev/xvda"
MOUNTPOINT="/mnt/xvda"

echo "Updating fstab"
LINE="${DISK}\t${MOUNTPOINT}\text4\tdefaults,nofail,discard\t0\t2"
cp /etc/fstab /tmp
echo -e ${LINE} >> /tmp/fstab
sudo mv /tmp/fstab /etc/fstab

echo "Mounting the disk"
sudo mkdir -p ${MOUNTPOINT}
sudo mount -o discard ${DISK} ${MOUNTPOINT}
