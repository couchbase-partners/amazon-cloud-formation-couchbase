# Generator

This is an CFT generator for Couchbase.  It creates templates that leverage XDCR and MDS.

## Extremely Important Note!

This doesn't work yet.

## Deployment

Creating a deployment is really simple.  Run the `deploy.sh` command with the name of a parameters file and the name of a [stack set](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html) to create.  For instance:

    ./deploy.sh simple simple_stack_set

The generator will create CFTs called `generatedTemplateX.json` that matches the specs in the parameter file and deploy them to AWS.
