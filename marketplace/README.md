# marketplace

This is an Amazon Cloud Formation (CFn) template that installs Couchbase Enterprise.  You can run it from the AWS CLI or using the web console.

# Deploy with the AWS CLI

## Environment Setup

You will need an AWS account with permission to access a variety of services including Cloud Formation, EC2 and EBS.

Now install and configure the AWS CLI.  Follow the instructions Amazon provides [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Basically all you need to do is:

    pip install --upgrade --user awscli
    aws configure

You can confirm the cli is working properly by running:

    aws ec2 describe-account-attributes

Then you'll want to clone this repo.  You can do that with the command:

    git clone https://github.com/couchbase-partners/amazon-cloud-formation-couchbase.git

## Creating a Stack

The AWS word for a deployment is a stack.  You can create a new stack using this template by running the commands:

    cd amazon-cloud-formation-couchbase
    cd simple
    ./deploy.sh <STACK_NAME>

When complete you can access the Couchbase web administrator tool on port 8091 of any node.

## Deleting a Stack

To delete your deployment you can either run the wrapper command below or use the GUI in the web console [here](https://console.aws.amazon.com/cloudformation/home).

    aws cloudformation delete-stack --stack-name <STACK_NAME>

## Next Steps

The getting started guide [here](https://www.couchbase.com/get-started-developing-nosql) is a great place to go next.
