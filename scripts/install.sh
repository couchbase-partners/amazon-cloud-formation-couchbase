#!/usr/bin/env bash

echo "Running install.sh"

# Using these instructions
# https://developer.couchbase.com/documentation/server/4.6/install/rhel-suse-install-intro.html
rpm --install couchbase-server-enterprise-4.6.1-centos7.x86_64.rpm

# Warning: Transparent hugepages looks to be active and should not be.
# Please look at http://bit.ly/1ZAcLjD as for how to PERMANENTLY alter this setting.

# Warning: Swappiness is not set to 0.
# Please look at http://bit.ly/1k2CtNn as for how to PERMANENTLY alter this setting.

# Not sure what this is about
# /var/tmp/rpm-tmp.IzbQ9i: line 6: systemctl: command not found
# /var/tmp/rpm-tmp.IzbQ9i: line 9: systemctl: command not found
