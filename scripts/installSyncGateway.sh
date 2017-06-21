#!/usr/bin/env bash

echo "Running installSyncGateway.sh"

wget https://packages.couchbase.com/releases/couchbase-sync-gateway/1.4.1/couchbase-sync-gateway-enterprise_1.4.1-3_x86_64.rpm
rpm -i couchbase-sync-gateway-enterprise_1.4.1-3_x86_64.rpm
