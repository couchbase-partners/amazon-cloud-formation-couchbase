# Marketplace

This template is used by the Couchbase Amazon Marketplace offer.  It is not intended to be used outside the marketplace.  Unless you are working on updates to the Couchbase Marketplace offer, you probably want to be using the [simple](../simple) template.

## Build AMI

This describes how we build the AMIs for the Couchbase AWS Marketplace offers.  This is provided for background.  A user of these templates does not need to complete this process.

Get a local copy of the Couchabse Server rpm by downloading them from https://www.couchbase.com/downloads

Alternatively you can run the command:

    wget https://packages.couchbase.com/releases/4.6.3/couchbase-server-enterprise-4.6.3-centos6.x86_64.rpm

Note that the Amazon Linux image we're using runs best with the Redhat 7 version of Couchbase Server

Login to the AWS Marketplace Management Portal and click on AMI.  [Here](https://aws.amazon.com/marketplace/management/manage-products) is a direct link.

Click to upload the RPM.  Note it takes several minutes to be reflected in the UI.

For AMI description use either:
* Couchbase Server Enterprise Edition 4.6.2
* Couchbase Sync Gateway Enterprise Edition 1.4.1-3

For the base AMI select Amazon Linux.

Then click build.  That's it!

## Update Listings

The offer is updated in the portal [here](https://aws.amazon.com/marketplace/management/).  The portal has a GUI to do updates, but we've had some issues with it.  For that reason, we've been using the product load form.  AWS can provide the latest product load form for what is "on site."  That can then be modified and loading into the portal.  This is the process we currently recommend.
