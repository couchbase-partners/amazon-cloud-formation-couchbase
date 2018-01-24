# Marketplace

This template is used by the Couchbase Amazon Marketplace offer.  It is not intended to be used outside the marketplace.  Unless you are working on updates to the Couchbase Marketplace offer, you probably want to be using a different template.

## Build AMIs

This describes how we build the AMIs for the Couchbase AWS Marketplace offers.  This is provided for background.  A user of these templates does not need to complete this process.

Get a local copy of the Couchbase Server and Sync Gateway RPMs:

    wget https://packages.couchbase.com/releases/4.6.4/couchbase-server-enterprise-4.6.4-centos6.x86_64.rpm
    wget https://packages.couchbase.com/releases/5.0.0/couchbase-server-enterprise-5.0.1-centos6.x86_64.rpm
    wget https://packages.couchbase.com/releases/couchbase-sync-gateway/1.5.1/couchbase-sync-gateway-enterprise_1.5.1_x86_64.rpm

Note that the Amazon Linux image we're using runs best with the CentOS 6 version of Couchbase Server.

Login to the AWS Marketplace Management Portal and click on AMI.  [Here](https://aws.amazon.com/marketplace/management/manage-products) is a direct link.

Click to upload the RPM.  Note it takes several minutes to be reflected in the UI.  The progress meter doesn't work in Chrome on the Mac, so use Safari instead.

For AMI description use one of:
* Couchbase Server Enterprise Edition 4.6.4
* Couchbase Server Enterprise Edition 5.0.1
* Couchbase Sync Gateway Enterprise Edition 1.5.1

For the base AMI select Amazon Linux.

Then click build.

## Clone AMIs

Once the AMI is built, send an email to aws-marketplace-seller-ops@amazon.com asking them to clone the AMI.  That will give an AMI for both Hourly Pricing and BYOL in every available region.  Even though the bits of all these AMIs are identical, there will be distinct AMI IDs for each one.  

They'll need to know the version number and release notes.

## Update Listings

The offer is updated in the portal [here](https://aws.amazon.com/marketplace/management/).  The portal has a GUI to do updates, but we've had some issues with it.  For that reason, we've been using the product load form.  AWS can provide the latest product load form for what is "on site."  That can then be modified and loading into the portal.  This is the process we currently recommend.
