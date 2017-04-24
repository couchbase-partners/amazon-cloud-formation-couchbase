#!/usr/bin/env bash

# Need to add an EBS drive to the CFn and configure it here.

mkdir -p /datadisks/disk1
chown -R couchbase /datadisks/disk1
chgrp -R couchbase /datadisks/disk1
