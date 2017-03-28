# Best Practices

## Compute

* R3
* R4
* M4

Placement groups?

### Memory Allocation

Q: We're currently doing 50% for data and 15% for index.  Need a good solution here.

### Fault Tolerance and High Availability

AZ mapping determined by autoscaling group

## Storage

EBS gp2

## Network

Use public IP.  Do we need 10G, balance against complexity of placement groups?

### Security

A number of steps are necessary to secure a Couchbase cluster:
* Configure authentication for the administrator tool
* Enable SSL for traffic between nodes
* Enable authentication for connections to the database as well.
