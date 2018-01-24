#######################################################"
############## Install Couchbase Server ###############"
#######################################################"
echo "Installing Couchbase Server..."

version=5.0.1
wget https://packages.couchbase.com/releases/${version}/couchbase-server-enterprise-${version}-centos6.x86_64.rpm
rpm --install couchbase-server-enterprise-${version}-centos6.x86_64.rpm

#######################################################"
############ Turn Off Transparent Hugepages ###########"
#######################################################"
echo "Turning off transparent hugepages..."

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

#######################################################
################# Set Swappiness to 0 #################
#######################################################
echo "Setting swappiness to 0..."

sysctl vm.swappiness=0
echo "
# Required for Couchbase
vm.swappiness = 0
" >> /etc/sysctl.conf
