# Best Practices

## Compute

A variety of compute types are EBS optimized.  Any such node will work well with Couchbase, though some may be more cost effective.  R4 and M4 machines are the most commonly used.  While one core machines will deploy successfully, [we recommend machines with 4 or more cores](https://developer.couchbase.com/documentation/server/current/install/pre-install.html) for production applications.

For a majority of applications the r4.4xlarge will be a good balance of price and performance.

We recommend using Autoscaling Groups instead of stand alone instances as it improves reliability and simplifies the addition and removal of nodes.

### Memory Allocation

Couchbase recommends allocating 85% of system memory to the database.  When using MDS this can be tuned between data, query, etc.  The templates currently allocate 50% for data and 15% for index.  This can be adjusted after deployment.

### Fault Tolerance and High Availability

Couchbase is a strongly consistent database with peer-to-peer replication for handling node failures.  Replicas are not needed to increase read performance due to a built-in managed caching layer.  For deployments in AWS, we typically recommend one replica.  In the event of a single node failure, replicas elsewhere in the cluster can be automatically promoted if automatic failover is [enabled](https://developer.couchbase.com/documentation/server/current/clustersetup/automatic-failover.html).  For most scenarios, the downed node will recover in a matter of minutes, obviating the need for additional replicas.

A minimum of 3 nodes required for the data service to support automatic failover, and a minimum of two nodes for the query, index and FTS service to support high availability.  Depending on your performance and topology needs, these services can be collocated or separated but the minimum node count requirement does not change.

The Couchbase concept of a Server Group maps closely to an Availability Zone (AZ).  We suggest deploying nodes across all available AZs and then creating a Couchbase Server Group per AZ.

## Storage

Amazon offers numerous storage options for IaaS.  When running Couchbase, three are viable:

* EBS gp2
* EBS io1
* SSD Instance Store

io1 is the most performant, but can be expensive.  For most applications, gp2 providers a good balance of performance and cost.  Instance stores are both performant and side step noisy neighbor issues that can potentially plague EBS.  However the instance store is ephemeral.  The persistence of EBS offers a significant advantage and is what we have chosen to provision in the CFn templates.

We recommend a 1TB EBS drive as the upper end.  Large drives can lead to overly dense nodes that suffer from long rebuild times.  It's usually preferable to scale horizontally instead.

## Network

Amazon provides a number of network options, including public DNS, VPN gateways and Direct Connect.  We recommend using public DNS for most applications.  They perform very well, are extremely cost effective and are resilient to failure.

The templates configure each Couchbase node with the public DNS.  In AWS the public DNS resolves to a NAT based IP from outside the VPC and to the private IP from within the VPC.  AWS refers to this as split brain DNS.

For applications where nodes may be stopped and started, you could use an Elastic IP (EIP).  However, that adds significant management complexity.  We do not recommend EIPs for most applications.

Placement groups provide 10G network, which is preferable.  However, they make the use of an Autoscaling Group more difficult as nodes will not be automatically spread across Availability Zones.  In the CFT, we've opted for simplicity.

### Security

The template automatically sets up a username and password for the Couchbase Web Administrator.  The template also configures a Security Group that closes off unused ports.  This configuration can be further secured by specifying CIDR blocks to whitelist and blocking others.

AWS [automatically enables encryption](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html) for disks that use EBS.

The template does not currently configure SSL.  We recommend setting it up for production applications.

These templates open Sync Gateway access to the internet over ports 4984 and 4985.  We typically recommend securing the admin interface for access from `127.0.0.1` only.  That can be done by editing the `/home/sync_gateway/sync_gateway.json` file.
