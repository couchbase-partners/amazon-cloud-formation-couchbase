# Generator

This is an CFT generator for Couchbase.  It creates templates that leverage MDS.  This template can be deployed in different regions for XDCR.

## Extremely Important Note!

This doesn't work yet.

## Deployment

Creating a deployment is really simple.  Run the `deploy.sh` command with the name of a parameters file and the name of a stack to create.  For instance:

    ./deploy.sh simple simple_stack

The generator will create a CFT called `generated.template` that matches the specs in the parameter file and deploy it to AWS.
