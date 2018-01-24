# Marketplace

This template is used by the Couchbase Amazon Marketplace offer.  It is not intended to be used outside the marketplace.  Unless you are working on updates to the Couchbase Marketplace offer, you probably want to be using a different template.

## Build AMIs

This describes how we build the AMIs for the Couchbase AWS Marketplace offers.  This is provided for background.  A user of these templates does not need to complete this process.

You'll need to get a local copy of the Couchbase Server and Sync Gateway RPMs:

    wget https://packages.couchbase.com/releases/4.6.4/couchbase-server-enterprise-4.6.4-centos6.x86_64.rpm
    wget https://packages.couchbase.com/releases/5.0.1/couchbase-server-enterprise-5.0.1-centos6.x86_64.rpm
    wget https://packages.couchbase.com/releases/couchbase-sync-gateway/1.5.1/couchbase-sync-gateway-enterprise_1.5.1_x86_64.rpm

Note that the Amazon Linux image we're using runs best with the CentOS 6 version of Couchbase Server.

Login to the AWS Marketplace Management Portal and click on Packages.  [Here](https://aws.amazon.com/marketplace/management/manage-packages/) is a direct link.

For the package name enter one of:

* Couchbase_Server_5-0-1_Amazon_Linux
* Couchbase_Server_4-6-4_Amazon_Linux
* Couchbase_Sync_Gateway_1-5-1_Amazon_Linux

Click to upload the RPM and the install.sh script.  Set install.sh as the installer package.

For the base AMI select Amazon Linux 2017.09.

Then click submit.

## Test AMIs

The AMIs are in us-east-1.  You can test deploying them using the AWS CLI and the command:

    aws blah blah

You'll want to ensure THP and swappiness are set and that Server is running on 8091 or Sync Gateway is running on 4985.

## Clone AMIs

Once the AMI is built, send an email to aws-marketplace-seller-ops@amazon.com asking them to clone the AMI.  That will give an AMI for both Hourly Pricing and BYOL in every available region.  Even though the bits of all these AMIs are identical, there will be distinct AMI IDs for each one.  

They'll need to know the version number and release notes.

## Update Listings

The offer is updated in the portal [here](https://aws.amazon.com/marketplace/management/).  The portal has a GUI to do updates, but we've had some issues with it.  For that reason, we've been using the product load form.  AWS can provide the latest product load form for what is "on site."  That can then be modified and loading into the portal.  This is the process we currently recommend.
