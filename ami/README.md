# Build AMI

This README describes how we build the AMI that the templates use. Users should not need to do this.

## Prerequisites

You'll need....

* java (for the amazon ec2 API tools)
* JAVA_HOME environment variable properly pointed at your java.

## Get the scripts

    git clone git@github.com:couchbaselabs/couchbase-ami.git
    cd couchbase-ami

## Setup credentials

    mkdir -p ~/.ec2/couchbase_aws-marketplace

Get the pk/cert for the marketplace-related AWS account.  They'll need to live at...

    ~/.ec2/couchbase_aws-marketplace/pk-RPGT6DCSVXNK5QWMHAACI3KUHN5ILKOX.pem
    ~/.ec2/couchbase_aws-marketplace/cert-RPGT6DCSVXNK5QWMHAACI3KUHN5ILKOX.pem

If your private keys and certs are in a different place, you can
override them by specifying them as KEY=value parameters to the make
command...

    make EC2_PRIVATE_KEY=MyLocationToPrivateKeyPEMFile \
         EC2_CERT=MyLocationToPrivateKeyPEMFile \
         clean

Get your ssh key so you can login into the EC2 instances.  These
usually will live in the ~/.ssh directory on your computer.  For example, mine is at...

    ~/.ssh/steveyen-key2

If you don't have an AMI compatible ssh key, run the following command to generate a new one

    make SSH_KEY=steveyen-key2 generate-key

# Building the AMI...

First, clean up from previous attempts...

    make clean

Then, if you're making an AMI for a version number update, be sure to
have the right tag.

Then, use step 0, which should launch an new EC2 instance.

    make SSH_KEY=steveyen-key2 step0

use step 1 could update the seed AMI for you.

    make SSH_KEY=steveyen-key2 step1

Alternatively, you could config it manully, or jump to step 2

If that takes longer than usual (because EC2 cloud is impacted), then repeat the following command untill you finally see some ec2-xxxxxx.compute-1.amazonaws.com addresses in the output...

    make SSH_KEY=steveyen-key2 instance-describe

You'll want to see output lines that look like...

    INSTANCE	i-936991f0	ami-7341831a	ec2-107-22-35-176.compute-1.amazonaws.com	ip-10-93-70-157.ec2.internal	running	steveyen-key2	0		m1.xlarge	2011-10-26T22:59:43+0000	us-east-1c	aki-825ea7eb			monitoring-disabled	107.22.35.176	10.93.70.157			ebs					paravirtual	xen		sg-dddbcdb4	default

Note: should update EC2 instance here before preoceeding with further installation.

    make SSH_KEY=john-key2 instance-clean
    make SSH_KEY=john-key2 instance-update

The previous might fail due to SSH issues.  Have patience, wait and
try again a few time, as the instance requires time to come online.

Reboot the instance from AWS UI to get the updated instance

Then, go to the next step, etc...

    make SSH_KEY=steveyen-key2 step2
    make SSH_KEY=steveyen-key2 step3
    make SSH_KEY=steveyen-key2 step5

By default, couchbase 2.0.0 will be installed. Provide VERSION number to override this option.

    make SSH_KEY=steveyen-key2 VERSION=2.0.0 step2
    make SSH_KEY=steveyen-key2 step3
    make SSH_KEY=steveyen-key2 VERSION=2.0.0 step5

NOTE: Skip step 4 to create image only without volume attached to the AMI

NOTE: If you don't want the package pre-installed on the AMI, such as
to just get an empty-but-ready AMI for QE/testing, then just skip
step2.

You should now have an AMI that's AWS / ISV Marketplace ready.  But,
it might take a few minutes for AWS to finish building it (moving it
out of 'pending' state -- have patience).

Finally, for an AMI meant for the AWS / ISV Marketplace, grant
permission for AWS to access it...

    grant access to aws # 6795-9333-3241

# Other Hints:

If you're doing an updated AMI due to a new software release,
be sure to scrub any README's for changes, etc.

To make a community edition AMI, use something like...

    make IMAGE_DESC="pre-installed Couchbase Server 2.0.0, Community Edition, 64bit" \
         PKG_NAME=couchbase-server-community_x86_64_2.0.0.rpm \
         SSH_KEY=steveyen-key2 \
         clean step0 step1 ...
