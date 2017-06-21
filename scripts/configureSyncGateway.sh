#!/usr/bin/env bash

echo "Running configureSyncGateway.sh"

serverDNS=""

echo '
{
  "log": ["*"],
  "databases": {
    "db": {
      "server": "http://${serverDNS}:8091",
      "bucket": "default",
      "users": { "GUEST": { "disabled": false, "admin_channels": ["*"] } }
    }
  }
}
' > /home/sync_gateway/sync_gateway.json
