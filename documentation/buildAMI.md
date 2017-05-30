# Build AMI

This document describes how we build the AMIs for the Couchbase AWS Marketplace offers.  This is provided for background.  A user of these templates does not need to complete this process.

## Instructions

Get a local copy of the Couchabse Server rpm by downloading them from https://www.couchbase.com/downloads

Note that the Amazon Linux image we're using runs best with the Redhat 7 version of Couchbase Server

Login to the AWS Marketplace Management Portal and click on AMI.  [Here](https://aws.amazon.com/marketplace/management/manage-products) is a direct link.

Click to upload the RPM.  Note it takes several minutes to be reflected in the UI.

For AMI description use either:
* Couchbase Server Enterprise Edition 4.6.2
* Couchbase Sync Gateway Enterprise Edition 1.4.1-3

For the base AMI select Amazon Linux.

Then click build.  That's it!
