# Marketplace

This template is used by the Couchbase Amazon Marketplace offer.  It is not intended to be used outside the marketplace.  Unless you are working on updates to the Couchbase Marketplace offer, you probably want to be using a different template.

## Build AMIs

This describes how we build the AMIs for the Couchbase AWS Marketplace offers.  This is provided for background.  A user of these templates does not need to complete this process.

Login to the AWS Marketplace Management Portal and click on Packages.  [Here](https://aws.amazon.com/marketplace/management/manage-packages/) is a direct link.

For the package name enter one of:

* Couchbase_Server_5-0-1
* Couchbase_Server_4-6-4
* Couchbase_Sync_Gateway_1-5-1

Click to upload the either installServer.sh or installSyncGateway.sh and select "Set as installer."

For the base AMI select Amazon Linux 2017.09.

Then click submit.

## Test AMIs

The AMIs are in us-east-1.  You can test deploying them using the AWS CLI and the command:

    aws ec2 run-instances \
      --image-id ami-a4f4c4de \
      --count 1 \
      --instance-type m4.xlarge \
      --key-name partnership-us-east-1 \
      --subnet-id subnet-00d1e577 \
      --security-group-ids sg-91bf0ff6

You'll want to ensure THP and swappiness are set to never by running the commands:

    cat /sys/kernel/mm/\*transparent_hugepage/enabled
    cat /sys/kernel/mm/\*transparent_hugepage/enabled
    cat /sys/kernel/mm/\*transparent_hugepage/defrag

You'll also want to check that either Server is running on 8091 or Sync Gateway is running on 4985.

Be sure to delete the instances and their drives when done.

## Clone AMIs

Once the AMI is built, send an email to aws-marketplace-seller-ops@amazon.com asking them to clone the AMI.  That will give an AMI for both Hourly Pricing and BYOL in every available region.  Even though the bits of all these AMIs are identical, there will be distinct AMI IDs for each one.  

They'll need to know the version number and release notes.

## Update Listings

The offer is updated in the portal [here](https://aws.amazon.com/marketplace/management/).  The portal has a GUI to do updates, but we've had some issues with it.  For that reason, we've been using the product load form.  AWS can provide the latest product load form for what is "on site."  That can then be modified and loading into the portal.  This is the process we currently recommend.
