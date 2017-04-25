#!/usr/bin/env bash

mkdir /mnt/datadisk
chown couchbase /mnt/datadisk
chgrp couchbase /mnt/datadisk
mount -a /dev/sdk /mnt/datadisk
