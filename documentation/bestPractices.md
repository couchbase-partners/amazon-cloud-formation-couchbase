# Best Practices

## Compute

Numerous AWS machine types are viable for running Couchbase.  Some commonly used instance types include:

All services on all nodes
* some instance types
* R3.2xlarge

Using MDS
Data - R3.2xlarge, R4.2xlarge
Query - C4.2xlarge
Index - ...

* R3
* R4
* M4

### Memory Allocation

Q: We're currently doing 50% for data and 15% for index.  Need a good solution here.

### Fault Tolerance and High Availability

The Couchbase concept of a Server Group maps closely to an Availability Zone.  We are currently working to automate the mapping in the CFn templates.

... best practices vs getting started

## Storage

Amazon offers numerous storage options for IaaS.  When running Couchbase, three are viable:

* EBS gp2
* EBS io1
* SSD Instance Store

io1 is the most performant, but can be expensive.  For most applications, gp2 providers a good balance of performance and cost.  Instance stores are both performant and side step noisy neighbor issues that can potentially plague EBS.  However the instance store is ephemeral.  The persistence of EBS offers a significant advantage and is what we have chosen to provision in the CFn templates.

--- add something about size.  up to about 1TB/node

## Network

Amazon provides a number of network options, including public IPs, VPN gateways and Direct Connect.  We recommend using public IPs for most applications.  They perform very well, are extremely cost effective and are resilient to failure.

EIP... try accessing cluster over PIP.  If not, need EIP per node because those will resolve public and private.

Pass public DNS to couchbase

Placement groups provide 10G network, which is preferable.  However, they make the use of an Autoscaling Group more difficult as nodes will not be automatically spread across Availability Zones.  In the CFn template, we've opted for simplicity.

### Security

A number of steps are necessary to secure a Couchbase cluster:
* Configure authentication for the administrator tool
* Enable SSL for traffic between nodes
* Enable authentication for connections to the database as well.
