# AWS Well-Architected Framework Review
As part of the Couchbase partnership with AWS, we are working to ensure compliance with the [AWS Well-Architected Framework](https://d0.awsstatic.com/whitepapers/architecture/AWS_Well-Architected_Framework.pdf).  This document describes that effort.

# Reference Architecture

For the purpose of this review we are considering a single Couchbase cluster deployed in a region with nodes in two different availability zones.

![](./images/wa-architecture.png)

The Couchbase CFn template [here](../marketplace/couchbase.template) creates an autoscaling group with four nodes by default.  The number of nodes is exposed as a parameter the user can select.  Those nodes should be split between two availability zones.  Each node has two EBS volumes attached, one for the OS disk and another for the data disk.  Those volumes use gp2.

# Out of Scope
More complex topologies, not described in this document, might include deployment with multiple clusters in different regions using Couchbase XDCR.  More complex deployments might also include the Couchbase MDS feature with nodes in a single cluster deployed in multiple autoscaling groups.  Finally, the Couchbase Sync Gateway could be deployed in any of these scenarios.

# Security Pillar

## SEC 1. How are you protecting access to and use of the AWS root account credentials?
The CFn template is not using the root account.  A user is configured for the VMs, but that is not used by Couchbase or the startup scripts.

## SEC 2. How are you defining roles and responsibilities of system users to control human access to the AWS Management Console and API?
The CFn template is not defining users to manage the console.

## SEC 3. How are you limiting automated access to AWS resources? (e.g., applications, scripts, and/or third-party tools or services)
In the template we grant minimal permissions for describing autoscaling groups and instances [here](../marketplace/couchbase.template#L306-L307).  Those are used by the startup script that configures Couchbase.

## SEC 4. How are you capturing and analyzing logs?
The Couchbase Administrator provides the ability to view logs.  Those logs can also be viewed from the command line.  Customers can also upload logs to Couchbase support.  The documentation for logs is [here](https://developer.couchbase.com/documentation/server/4.6/clustersetup/ui-logs.html).

## SEC 5. How are you enforcing network and host-level boundary protection?
The template [defines a security group](../marketplace/couchbase.template#L317) that blocks ports Couchbase does not use.  For scenarios where remote developer access and XDCR are not required, it's possible to further restrict accesss by configuring the RemoteAccessCIDR [here](../marketplace/couchbase.template#L34).

## SEC 6. How are you leveraging AWS service level security features?
The Couchbase CFn template uses the following AWS services:
* IAM - The template defines minimal roles with describe access for VMs and autoscaling groups
* EC2 - The template configures a security group with minimal access and the option to close access entirely via a configurable CIDR block.
* EBS - The template defines EBS drives that a user could configure to use encryption.

## SEC 7. How are you protecting the integrity of the operating systems on your Amazon EC2 instances?
Couchbase binaries are made available with an MD5 checksum a user can use to validate the binary.  We do not have a process in place to checksum deployed binaries.

## SEC 8. How are you classifying your data?
Couchbase is a database.  Data stored in Couchbase in stored in buckets.  Each bucket can have its own security configuration.  That is documented [here](https://developer.couchbase.com/documentation/server/current/security/security-authentication.html#topic_ztr_rnm_lq).

## SEC 9. How are you encrypting and protecting your data at rest?
The template configures Couchbase to store data on a dedicated EBS drive.  A user can chose to enable encryption on that drive.  Couchbase also has a partner ecosystem that can provide encryption at rest if a user choses to deploy on an instance store.  Detail on that is available [here](https://developer.couchbase.com/documentation/server/4.6/security/security-data-encryption.html).

## SEC 10. How are you managing keys?
The template takes a key as input, but does not manage keys directly.

## SEC 11. How are you encrypting and protecting your data in transit?
Couchbase uses TLS/SSL to encrypt communications node to node and drive to node.  That is detailed [here](https://developer.couchbase.com/documentation/server/4.6/security/security-comm-encryption.html).

## SEC 12. How do you ensure you have the appropriate incident response?
Couchbase recommends following the security best practices [here](https://developer.couchbase.com/documentation/server/4.6/security/security-best-practices.html).  For specific incident response, customers should work with their security office and involve Couchbase and AWS support as required.

# Reliability Pillar

## REL 1. How do you manage AWS service limits for your accounts?
Couchbase does not manage AWS service limits.

## REL 2. How are you planning your network topology on AWS?
The template configures each Couchbase node with its public DNS record.  With AWS split brain DNS, that record resolves to the private IP when invoked from inside the node's VPC.  It resolves to the public IP when invoked from elsewhere.  For the single cluster deployment in scope for this document, this configuration is substantially equivalent to configuring with private DNS.

## REL 3. How does your system adapt to changes in demand?
Autoscaling a database is difficult.  In the event of increased demand, we recommend that an administrator identify the need and add or remove a node.  Cluster operations are documented [here](https://developer.couchbase.com/documentation/server/4.6/clustersetup/server-setup.html).

## REL 4. How are you monitoring AWS resources?
The Couchbase Administrator provides a single pane of glass for monitoring.  Documentation is available [here](https://developer.couchbase.com/documentation/server/4.6/monitoring/monitor-intro.html).

## REL 5. How are you executing change?
Couchbase does not automate upgrades.  Documentation for upgrades is given [here](https://developer.couchbase.com/documentation/server/4.6/install/upgrade.html).

## REL 6. How are you backing up your data?
Couchbase provides tools to backup and recover the database.  Those are invoked manually by a user.  Documentation is [here](https://developer.couchbase.com/documentation/server/4.6/backup-restore/backup-restore.html).

## REL 7. How does your system withstand component failures?
Couchbase is resilient to a variety of failure scenarios.  Node reboots and minimal downtime may not even require an operational response.

Failure scenarios:
* EBS disk failure - handled transparently by AWS
* Permanent node failure - handled transparently by AWS
* Availability zone failure - resilient through server groups
* Region failure - In scope wait for reboot and potentially recover from backup.  Out of scope XDCR could assist.
* Control plane failure - Wait for AWS recovery
* Network failure - discuss what kind

## REL 8. How are you testing for resiliency?
Couchbase QA tests a variety of failure scenarios for each release of the product.

## REL 9. How are you planning for disaster recovery?
For a single cluster configuration, Couchbase is deployed across two availability zones and resilient to failure of a zone.  If an entire region fails, restoration from a backup may be required.

More advanced scenarios, out of scope here, might leverage [XDCR](https://developer.couchbase.com/documentation/server/4.6/xdcr/xdcr-intro.html) to avoid downtime in the event of a regional failure.

# Performance Pillar

## PERF 1. How do you select the best performing architecture?
Our engineering and business development teams partner with AWS to select the optimal components for running Couchbase.  The CFn templates are the result of years of experience from the Couchbase services and support organizations deploying at some of the largest enterprises in the world, including joint customers like [Viber](https://www.couchbase.com/customers/viber) and [RyanAir](https://www.couchbase.com/customers/ryanair).

## PERF 2. How do you select your compute solution?
Compute nodes are selected in accordance with Couchbase documentation [here](https://developer.couchbase.com/documentation/server/4.6/install/pre-install.html).  For most use cases we recommend EBS optimized machines as a variety of operational issues are simplified through the use of EBS rather than an instance store.

## PERF 3. How do you select your storage solution?
Couchbase can work on a variety of AWS storage solutions.  These are:

* EBS io1
* EBS gp2
* SSD instance store

We find EBS gp2 to be a good balance of performance and cost for most applications.  It also provides operational benefits over the instance store.  We do not recommend any HDD storage as its performance characteristics are insufficient for Couchbase.

## PERF 4. How do you select your database solution?
Couchbase is a database.

## PERF 5. How do you select your network solution?
For the single cluster deployment described in this document the default network works well.  More complex topolgies that include XDCR may necessitate the use of transit VPCs, public IPs or Direct Connect.

## PERF 6. How do you ensure that you continue to have the most appropriate resource type as new resource types and features are introduced?
Our engineering and business development partner with AWS to evaluate and incorporate new features.

## PERF 7. How do you monitor your resources post-launch to ensure they are performing as expected?
The Couchbase Administrator provides a variety of performance metrics.  Those are documented [here](https://developer.couchbase.com/documentation/server/4.6/monitoring/monitor-intro.html).  In addition, a user can make use of the AWS Console and native AWS tools to supplement this monitoring.

## PERF 8. How do you use tradeoffs to improve performance?
Depending on a customer's use case, Couchbase can be configured in a variety of ways.  Nodes can be selected to favor different Couchbase services - data, index, query, full text search.  Additionally, nodes can be selected to store all or a small portion of data in memory.  If all data can be cached in memory, performance will be better, but at a greater financial cost.

# Cost Optimization Pillar

## COST 1. Are you considering cost when you select AWS services for your solution?
Yes!  We use commodity resources where possible on AWS.  This includes EBS gp2, the generic network and dynamic ip addresses, all with the goal of minimizing cost while maximizing performance.

## COST 2. Have you sized your resources to meet your cost targets?
As the AWS resources are consumed by end customers, not Couchbase directly, we do not have cost targets.

## COST 3. Have you selected the appropriate pricing model to meet your cost targets?
As the AWS resources are consumed by end customers, not Couchbase directly, we do not have cost targets.

## COST 4. How do you make sure your capacity matches but does not substantially exceed what you need?
Both the Couchbase Administrator and the AWS Console provide monitoring that can indicate if a cluster is oversized for its workload.  Our documentation provides sizing guidelines [here](https://developer.couchbase.com/documentation/server/4.6/install/sizing-general.html).  The Couchbase solution engineering and solution architecture teams also aid our customers in picking the optimal hardware for their use case.

## COST 5. Did you consider data-transfer charges when designing your architecture?
Clusters are deployed across two availability zones.  We recommend defining server groups that map to those availability zones.  That ensures a copy of the data will reside in each zone.  Typically a customer would deploy their application in the same region, and potentially the same zone, as the database.  This further reduces cost.

## COST 6. How are you monitoring usage and spending?
Couchbase does not monitor AWS use.  Our customers can track their use with the tools that AWS provides.

## COST 7. Do you decommission resources that you no longer need or stop resources that are temporarily not needed?
No.  Autoscaling a database can lead to a variety of issues.  Customers can manually decommission nodes if they determine they are no longer needed.

## COST 8. What access controls and procedures do you have in place to govern AWS usage?
Couchbase does not govern AWS usage.

## COST 9. How do you manage and/or consider the adoption of new services?
Couchbase is currently deployed on AWS IaaS.  We make use of EC2, EBS, CFn, S3 and a variety of other AWS components.  We are constantly working with AWS to identify new areas we can collaborate.  We're a very customer driven organization and work closely with our customers to determine what new AWS services we should integrate with.

One of the most exciting is IoT.  Recent work on AWS IoT is described [here](https://blog.couchbase.com/aws-iot-button-lambda-couchbase/).  

# Operational Excellence Pillar

## OPS 1. What best practices for cloud operations are you using?
Formal documentation for best practices is [here](https://developer.couchbase.com/documentation/server/4.6/install/deployment-aws.html#story-h2-3).  We have an additional rough best practices document [here](bestPractices.md).

## OPS 2. How are you doing configuration management for your workload?
Couchbase does not prescribe a configuration management tool.  Our customers use a variety of tools in the marketplace, including Chef, Puppet and Ansible.  For our AWS partnership we are focusing on improving our CFn integation.

## OPS 3. How are you evolving your workload while minimizing the impact of change?
Couchbase is continually working on new versions of our software.  We recently announced 5.0 [here](https://www.couchbase.com/products/latest-innovations).  Every update of our software includes documentation for migration to the latest version.  As an example, [here](https://developer.couchbase.com/documentation/server/4.6/install/upgrade.html) is the documentation to upgrade to 4.6 from previous versions.

## OPS 4. How do you monitor your workload to ensure it is operating as expected?
The Couchbase Administrator provides a single pane of glass for monitoring.  Documentation is available [here](https://developer.couchbase.com/documentation/server/4.6/monitoring/monitor-intro.html)

## OPS 5. How do you respond to unplanned operational events?
Couchbase is an ISV.  we do not respond to operational failures.  Customers put in place their own processes for running Couchbase.  Our support team can support that.  Customers might select different support policies based on their requirements.  Those are detailed [here](https://www.couchbase.com/support-policy).

## OPS 6. How is escalation managed when responding to unplanned operational events?
Escalation is manual process that our customers chose based on their environment, use case and policies.  It is not prescribed by Couchbase.
