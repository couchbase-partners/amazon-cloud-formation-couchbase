# simple

This is an Amazon Cloud Formation (CFn) template that installs Couchbase Enterprise.  You can run it from the AWS CLI or using the web console.

# Deploy with the AWS CLI

## Environment Setup

You will need an AWS account with permission to access the services:
* Cloud Formation
* EC2
* EBS

First we need to install and configure the AWS CLI.  Follow the instructions Amazon provides [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Basically all you need to do is:

    pip install --upgrade --user awscli
    aws configure

You can confirm the cli is working properly by running:

    aws ec2 describe-account-attributes

Then you'll want to clone this repo.  You can do that with the command:

    git clone https://github.com/couchbase-partners/amazon-cloud-formation-couchbase.git

If you don't have a key, you'll also need to create one.  That can be done with these commands:

    REGION=`aws configure get region`
    KEY_NAME="couchbase-${REGION}"
    KEY_FILENAME=~/.ssh/${KEY_NAME}.pem
    if [ ! -e ${KEY_FILENAME} ]
    then
      echo "The key does not exist.  Generating a new key."
      aws ec2 create-key-pair --region ${REGION} --key-name ${KEY_NAME} --query 'KeyMaterial' --output text > ${KEY_FILENAME}
      chmod 600 ${KEY_FILENAME}
      echo "Key saved to ${KEY_FILENAME}"
    fi

## Creating a Stack

The AWS word for a deployment is a stack.  [deploy.sh](deploy.sh) is a helper script to deploy a stack.  Take a look at it and modify any variables, then run it as:

    cd amazon-cloud-formation-couchbase
    cd simple
    ./deploy.sh <STACK_NAME>

When complete you can access the Couchbase web administrator tool on port 8091 of any node.

## Deleting a Stack

To delete your deployment you can either run the wrapper command below or use the GUI in the web console [here](https://console.aws.amazon.com/cloudformation/home).

    aws cloudformation delete-stack --stack-name <STACK_NAME>

## Next Steps

The getting started guide [here](https://www.couchbase.com/get-started-developing-nosql) is a great place to go next.
