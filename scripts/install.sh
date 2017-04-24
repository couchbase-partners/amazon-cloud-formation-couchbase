#!/usr/bin/env bash

echo "Running install.sh"

# Using these instructions
# https://developer.couchbase.com/documentation/server/4.6/install/rhel-suse-install-intro.html
sudo yum install -y pkgconfig
rpm --install couchbase-server-enterprise-4.6.1-centos7.x86_64.rpm

#Warning: Transparent hugepages looks to be active and should not be.
#Please look at http://bit.ly/1ZAcLjD as for how to PERMANENTLY alter this setting.
