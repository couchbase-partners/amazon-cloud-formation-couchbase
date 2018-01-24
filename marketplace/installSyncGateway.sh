#######################################################"
########### Install Couchbase Sync Gateway ############"
#######################################################"
echo "Installing Couchbase Sync Gateway..."

version=1.5.1
wget https://packages.couchbase.com/releases/couchbase-sync-gateway/${version}/couchbase-sync-gateway-enterprise_${version}_x86_64.rpm
rpm --install couchbase-sync-gateway-enterprise_${version}_x86_64.rpm
