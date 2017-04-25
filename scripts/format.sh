#!/usr/bin/env bash

# Need to add an EBS drive to the CFn and configure it here.

mkdir /mnt/datadisk
chown couchbase /mnt/datadisk
chgrp couchbase /mnt/datadisk

#mount -a /dev/sdk /mnt/datadisk
