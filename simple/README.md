# simple

This is an Amazon Cloud Formation Template (CFT) that installs Couchbase Enterprise.  You can run it from the AWS CLI or using the web console.

# How To Video

[![IMAGE ALT TEXT](http://img.youtube.com/vi/KpwmiRKrsfw/0.jpg)](https://www.youtube.com/watch?v=KpwmiRKrsfw&index=4&list=PLG3nTnYVz3nzGsaREuEjlvAKnNe4Xc-8j "Deploying Couchbase with the AWS CLI and CloudFormation")

# Instructions

## Important Note

This template uses two AWS Marketplace AMIs.  To deploy in your AWS subscription you must first subscribe to the AMIs [here](https://aws.amazon.com/marketplace/seller-profile?id=1a064a14-5ac2-4980-9167-15746aabde72)

## Environment Setup

You will need an AWS account with these permissions:
* aws-marketplace:Subscribe
* aws-marketplace:ViewSubscriptions
* ec2:AuthorizeSecurityGroupEgress
* ec2:AuthorizeSecurityGroupIngress
* ec2:CreateSecurityGroup
* ec2:DescribeImages
* ec2:DescribeInstances
* ec2:DescribeKeyPairs
* ec2:DeleteSecurityGroup
* ec2:DescribeSecurityGroups
* ec2:DescribeSubnets
* ec2:DescribeVpcs
* ec2:DescribeAccountAttributes
* ec2:RunInstances
* ec2:StartInstances
* ec2:StopInstances
* ec2:TerminateInstances
* iam:AddRoleToInstanceProfile
* iam:CreateInstanceProfile
* iam:DeleteInstanceProfile
* iam:DeleteRole
* iam:DeleteRolePolicy
* iam:PassRole
* iam:PutRolePolicy
* iam:RemoveRoleFromInstanceProfile

First we need to install and configure the AWS CLI.  Follow the instructions Amazon provides [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Basically all you need to do is:

    pip install --upgrade --user awscli
    aws configure

You can confirm the CLI is working properly by running:

    aws ec2 describe-account-attributes

If you don't have a key, you'll also need to create one.  That can be done with these commands:

    REGION=`aws configure get region`
    KEY_NAME="couchbase-${REGION}"
    KEY_FILENAME=~/.ssh/${KEY_NAME}.pem
    aws ec2 create-key-pair \
      --region ${REGION} \
      --key-name ${KEY_NAME} \
      --query 'KeyMaterial' \
      --output text > ${KEY_FILENAME}
    chmod 600 ${KEY_FILENAME}
    echo "Key saved to ${KEY_FILENAME}"

Then you'll want to clone this repo.  You can do that with the command:

    git clone https://github.com/couchbase-partners/amazon-cloud-formation-couchbase.git
    cd amazon-cloud-formation-couchbase
    cd simple

## Creating a Stack

The AWS word for a deployment is a stack.  [deploy.sh](deploy.sh) is a helper script to deploy a stack.  Take a look at it and modify any variables, then run it as:

    ./deploy.sh <STACK_NAME>

When complete you can access the Couchbase web administrator tool on port 8091 of any Server node.

## Deleting a Stack

To delete your deployment you can either run the command below or use the GUI in the web console [here](https://console.aws.amazon.com/cloudformation/home).

    aws cloudformation delete-stack --stack-name <STACK_NAME>
