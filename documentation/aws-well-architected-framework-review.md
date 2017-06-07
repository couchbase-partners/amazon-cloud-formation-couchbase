# AWS Well-Architected Framework Review
As part of the Couchbase partnership with AWS, we are working to ensure compliance with the [AWS Well-Architected Framework](https://d0.awsstatic.com/whitepapers/architecture/AWS_Well-Architected_Framework.pdf).  This document describes that effort.

# Reference Architecture

For the purpose of this review we are considering a single Couchbase cluster deployed in a region with nodes in two different availability zones.

![](./images/wa-architecture.png)

The Couchbase CFn template [here](../marketplace/couchbase.template) creates an autoscaling group with four nodes by default.  The number of nodes is exposed as a parameter the user can select.  Those nodes should be split between two availability zones.  Each node has two EBS volumes attached, one for the OS disk and another for the data disk.  Those volumes use gp2.

The template configures each Couchbase node with its public DNS record.  With AWS split brain DNS, that record resolves to the private IP when invoked from inside the node's VPC.  It resolves to the public IP when invoked from elsewhere.

The template [defines a security group](../marketplace/couchbase.template#L317) that blocks ports Couchbase does not use.  For scenarios where remote developer access and XDCR are not required, it's possible to further restrict accesss by configuring the RemoteAccessCIDR [here](../marketplace/couchbase.template#L34).

# Out of Scope
More complex topologies, not described in this document, might include deployment with multiple clusters in different regions using Couchbase XDCR.  More complex deployments might also include the Couchbase MDS feature with nodes in a single cluster deployed in multiple autoscaling groups.  Finally, the Couchbase Sync Gateway could be deployed in any of these scenarios.

# Security Pillar

## SEC 1. How are you protecting access to and use of the AWS root account credentials?
The CFn template is not using the root account.  A user is configured for the VMs, but that is not used by Couchbase or the startup scripts.

## SEC 2. How are you defining roles and responsibilities of system users to control human access to the AWS Management Console and API?
The CFn template is not defining users to manage the console.  We believe this item is out of scope.

## SEC 3. How are you limiting automated access to AWS resources? (e.g., applications, scripts, and/or third-party tools or services)
In the template we grant minimal permissions for describing autoscaling groups and instances [here](../marketplace/couchbase.template#L306-L307).

## SEC 4. How are you capturing and analyzing logs?
## SEC 5. How are you enforcing network and host-level boundary protection?
## SEC 6. How are you leveraging AWS service level security features?
## SEC 7. How are you protecting the integrity of the operating systems on your Amazon EC2 instances?
## SEC 8. How are you classifying your data?
## SEC 9. How are you encrypting and protecting your data at rest?
## SEC 10. How are you managing keys?
## SEC 11. How are you encrypting and protecting your data in transit?
## SEC 12. How do you ensure you have the appropriate incident response?

# Reliability Pillar
## REL 1. How do you manage AWS service limits for your accounts?
## REL 2. How are you planning your network topology on AWS?
## REL 3. How does your system adapt to changes in demand?
## REL 4. How are you monitoring AWS resources?
## REL 5. How are you executing change?
## REL 6. How are you backing up your data?
## REL 7. How does your system withstand component failures?
## REL 8. How are you testing for resiliency?
## REL 9. How are you planning for disaster recovery?

# Performance Pillar
## PERF 1. How do you select the best performing architecture?
## PERF 2. How do you select your compute solution?
## PERF 3. How do you select your storage solution?
## PERF 4. How do you select your database solution?
## PERF 5. How do you select your network solution?
## PERF 6. How do you ensure that you continue to have the most appropriate resource type as new resource types and features are introduced?
## PERF 7. How do you monitor your resources post-launch to ensure they are performing as expected?
## PERF 8. How do you use tradeoffs to improve performance?

# Cost Optimization Pillar
## COST 1. Are you considering cost when you select AWS services for your solution?
## COST 2. Have you sized your resources to meet your cost targets?
## COST 3. Have you selected the appropriate pricing model to meet your cost targets?
## COST 4. How do you make sure your capacity matches but does not substantially exceed what you need?
## COST 5. Did you consider data-transfer charges when designing your architecture?
## COST 6. How are you monitoring usage and spending?
## COST 7. Do you decommission resources that you no longer need or stop resources that are temporarily not needed?
## COST 8. What access controls and procedures do you have in place to govern AWS usage?
## COST 9. How do you manage and/or consider the adoption of new services?

# Operational Excellence Pillar
## OPS 1. What best practices for cloud operations are you using?
## OPS 2. How are you doing configuration management for your workload?
## OPS 3. How are you evolving your workload while minimizing the impact of change?
## OPS 4. How do you monitor your workload to ensure it is operating as expected?
## OPS 5. How do you respond to unplanned operational events?
## OPS 6. How is escalation managed when responding to unplanned operational events?
