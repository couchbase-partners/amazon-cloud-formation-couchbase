import sys
import yaml
import json

def main():
    filename=sys.argv[1]
    print('Using parameter file: ' + filename)
    with open(filename, 'r') as stream:
        parameters = yaml.load(stream)
    print('Parameters: ' + str(parameters))

    template={
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "AWS Deployment for Couchbase Enterprise",
        "Parameters": {
            "Username": {
                "Description": "Username for Couchbase administrator",
                "Type": "String"
            },
            "Password": {
                "Description": "Password for Couchbase administrator",
                "Type": "String",
                "NoEcho": True
            },
            "KeyName": {
                "Description": "Name of an existing EC2 KeyPair",
                "Type": "AWS::EC2::KeyPair::KeyName"
            }
        },
        "Mappings": {},
        "Resources": {}
    }

    serverVersion = parameters['serverVersion']
    syncGatewayVersion = parameters['syncGatewayVersion']
    cluster = parameters['cluster']

    template['Mappings'] = dict(template['Mappings'].items() + generateMappings().items())
    template['Resources'] = dict(template['Resources'].items() + generateMiscResources().items())
    template['Resources'] = dict(template['Resources'].items() + generateCluster(serverVersion, syncGatewayVersion, cluster).items())

    file = open('generated.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()

def generateMappings():
    mappings = {
        "CouchbaseServer": {
            "us-east-1": { "BYOL": "ami-1853ac65", "HourlyPricing": "ami-1853ac65" },
            "us-east-2": { "BYOL": "ami-25615740", "HourlyPricing": "ami-25615740" },
            "us-west-1": { "BYOL": "ami-bf5540df", "HourlyPricing": "ami-bf5540df" },
            "us-west-2": { "BYOL": "ami-d874e0a0", "HourlyPricing": "ami-d874e0a0" },
            "ca-central-1": { "BYOL": "ami-5b55d23f", "HourlyPricing": "ami-5b55d23f" },
            "eu-central-1": { "BYOL": "ami-ac442ac3", "HourlyPricing": "ami-ac442ac3" },
            "eu-west-1": { "BYOL": "ami-3bfab942", "HourlyPricing": "ami-3bfab942" },
            "eu-west-2": { "BYOL": "ami-dff017b8", "HourlyPricing": "ami-dff017b8" },
            "eu-west-3": { "BYOL": "ami-4f55e332", "HourlyPricing": "ami-4f55e332" },
            "ap-southeast-1": { "BYOL": "ami-e2adf99e", "HourlyPricing": "ami-e2adf99e" },
            "ap-southeast-2": { "BYOL": "ami-43874721", "HourlyPricing": "ami-43874721" },
            "ap-northeast-1": { "BYOL": "ami-a77c30c1", "HourlyPricing": "ami-a77c30c1" },
            "ap-northeast-2": { "BYOL": "ami-5e1ab730", "HourlyPricing": "ami-5e1ab730" },
            "ap-south-1": { "BYOL": "ami-7c87d913", "HourlyPricing": "ami-7c87d913" },
            "sa-east-1": { "BYOL": "ami-5339733f", "HourlyPricing": "ami-5339733f" },
            "us-gov-west-1": { "BYOL": "ami-2b39b24a", "HourlyPricing": "ami-2b39b24a" }
        },
        "CouchbaseSyncGateway": {
            "us-east-1": { "BYOL": "ami-1853ac65", "HourlyPricing": "ami-1853ac65" },
            "us-east-2": { "BYOL": "ami-25615740", "HourlyPricing": "ami-25615740" },
            "us-west-1": { "BYOL": "ami-bf5540df", "HourlyPricing": "ami-bf5540df" },
            "us-west-2": { "BYOL": "ami-d874e0a0", "HourlyPricing": "ami-d874e0a0" },
            "ca-central-1": { "BYOL": "ami-5b55d23f", "HourlyPricing": "ami-5b55d23f" },
            "eu-central-1": { "BYOL": "ami-ac442ac3", "HourlyPricing": "ami-ac442ac3" },
            "eu-west-1": { "BYOL": "ami-3bfab942", "HourlyPricing": "ami-3bfab942" },
            "eu-west-2": { "BYOL": "ami-dff017b8", "HourlyPricing": "ami-dff017b8" },
            "eu-west-3": { "BYOL": "ami-4f55e332", "HourlyPricing": "ami-4f55e332" },
            "ap-southeast-1": { "BYOL": "ami-e2adf99e", "HourlyPricing": "ami-e2adf99e" },
            "ap-southeast-2": { "BYOL": "ami-43874721", "HourlyPricing": "ami-43874721" },
            "ap-northeast-1": { "BYOL": "ami-a77c30c1", "HourlyPricing": "ami-a77c30c1" },
            "ap-northeast-2": { "BYOL": "ami-5e1ab730", "HourlyPricing": "ami-5e1ab730" },
            "ap-south-1": { "BYOL": "ami-7c87d913", "HourlyPricing": "ami-7c87d913" },
            "sa-east-1": { "BYOL": "ami-5339733f", "HourlyPricing": "ami-5339733f" },
            "us-gov-west-1": { "BYOL": "ami-2b39b24a", "HourlyPricing": "ami-2b39b24a" }
        }
    }
    return mappings

def generateMiscResources():
    resources = {
        "CouchbaseInstanceProfile": {
            "Type": "AWS::IAM::InstanceProfile",
            "Properties": {"Roles": [{"Ref": "CouchbaseRole"}]}
        },
        "CouchbaseRole": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"]},
                        "Action": ["sts:AssumeRole"]
                    }]
                },
                "Policies": [{
                    "PolicyName": "CouchbasePolicy",
                    "PolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Effect": "Allow",
                            "Action": [
                                "ec2:CreateTags",
                                "ec2:DescribeTags",
                                "ec2:DescribeInstances",
                                "autoscaling:DescribeAutoScalingGroups"
                            ],
                            "Resource": "*"
                        }]
                    }
                }]
            }
        },
        "CouchbaseSecurityGroup": {
            "Type": "AWS::EC2::SecurityGroup",
            "Properties": {
                "GroupDescription" : "Enable SSH and Couchbase Ports",
                "SecurityGroupIngress": [
                    { "IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 4369, "ToPort": 4369, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 4984, "ToPort": 4985, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 8091, "ToPort": 8096, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 9100, "ToPort": 9105, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 9110, "ToPort": 9122, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 9998, "ToPort": 9999, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 11207, "ToPort": 11215, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 18091, "ToPort": 18096, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 21100, "ToPort": 21299, "CidrIp": "0.0.0.0/0" }
                ]
            }
        }
    }
    return resources

def generateCluster(serverVersion, syncGatewayVersion, cluster):
    resources = {}
    rallyAutoScalingGroup=cluster[0]['group']
    for group in cluster:
        groupResources=generateGroup(serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup)
        resources = dict(resources.items() + groupResources.items())
    return resources

def generateGroup(serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup):
    resources = {}
    license=group['license']
    if 'syncGateway' in group['services']:
        resources = dict(resources.items() + generateSyncGateway(license, syncGatewayVersion, group, rallyAutoScalingGroup).items())
    else:
        resources = dict(resources.items() + generateServer(license, serverVersion, group, rallyAutoScalingGroup).items())
    return resources

def generateSyncGateway(license, syncGatewayVersion, group, rallyAutoScalingGroup):
    groupName = group['group']
    nodeCount = group['nodeCount']
    nodeType = group['nodeType']

    resources = {
        groupName + "AutoScalingGroup": {
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "AvailabilityZones": { "Fn::GetAZs": "" },
                "LaunchConfigurationName": { "Ref": groupName + "LaunchConfiguration" },
                "MinSize": 0,
                "MaxSize": 100,
                "DesiredCapacity": nodeCount
            }
        },
        groupName + "LaunchConfiguration": {
            "Type": "AWS::AutoScaling::LaunchConfiguration",
            "Properties": {
                "ImageId": { "Fn::FindInMap": [ "CouchbaseSyncGateway", { "Ref": "AWS::Region" }, "AMI" ] },
                "InstanceType": nodeType,
                "SecurityGroups": [ { "Ref": "CouchbaseSecurityGroup" } ],
                "KeyName": { "Ref": "KeyName" },
                "EbsOptimized": True,
                "IamInstanceProfile": { "Ref": "CouchbaseInstanceProfile" },
                "BlockDeviceMappings":
                [
                    {
                        "DeviceName" : "/dev/xvda",
                        "Ebs" : { "DeleteOnTermination" : True }
                    }
                ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": [ "", [
                            "#!/bin/bash\n",
                            "echo 'Running startup script...'\n",
                            "stackName=", { "Ref": "AWS::StackName" }, "\n",
                            "license=" + license + "\n",
                            "syncGatewayVersion=" + syncGatewayVersion + "\n",
                            "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
                            "wget ${baseURL}syncGateway.sh\n",
                            "chmod +x *.sh\n",
                            "./syncGateway.sh ${stackName} ${license} ${syncGatewayVersion}\n"
                        ]]
                    }
                }
            }
        }
    }
    return resources

def generateServer(license, serverVersion, group, rallyAutoScalingGroup):
    groupName = group['group']
    nodeCount = group['nodeCount']
    nodeType = group['nodeType']
    dataDiskSize = group['dataDiskSize']
    services = group['services']

    servicesParameter=''
    for service in services:
        servicesParameter += service + ','
    servicesParameter=servicesParameter[:-1]

    command = [
        "#!/bin/bash\n",
        "echo 'Running startup script...'\n",
        "adminUsername=", { "Ref": "Username" }, "\n",
        "adminPassword=", { "Ref": "Password" }, "\n",
        "services=" + servicesParameter + "\n",
        "stackName=", { "Ref": "AWS::StackName" }, "\n",
        "license=" + license + "\n",
        "serverVersion=" + serverVersion + "\n",
        "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
        "wget ${baseURL}server.sh\n",
        "wget ${baseURL}util.sh\n",
        "chmod +x *.sh\n",
    ]
    if groupName==rallyAutoScalingGroup:
        command.append("./server.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${license} ${serverVersion}\n")
    else:
        command.append("rallyAutoScalingGroup=")
        command.append({ "Ref": rallyAutoScalingGroup + "AutoScalingGroup" })
        command.append("\n")
        command.append("./server.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${license} ${serverVersion} ${rallyAutoScalingGroup}\n")

    resources = {
        groupName + "AutoScalingGroup": {
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "AvailabilityZones": { "Fn::GetAZs": "" },
                "LaunchConfigurationName": { "Ref": groupName + "LaunchConfiguration" },
                "MinSize": 1,
                "MaxSize": 100,
                "DesiredCapacity": nodeCount
            }
        },
        groupName + "LaunchConfiguration": {
            "Type": "AWS::AutoScaling::LaunchConfiguration",
            "Properties": {
                "ImageId": { "Fn::FindInMap": [ "CouchbaseServer", { "Ref": "AWS::Region" }, "AMI" ] },
                "InstanceType": nodeType,
                "SecurityGroups": [ { "Ref": "CouchbaseSecurityGroup" } ],
                "KeyName": { "Ref": "KeyName" },
                "EbsOptimized": True,
                "IamInstanceProfile": { "Ref": "CouchbaseInstanceProfile" },
                "BlockDeviceMappings":
                [
                    {
                        "DeviceName" : "/dev/xvda",
                        "Ebs" : { "DeleteOnTermination" : True }
                    },
                    {
                        "DeviceName" : "/dev/sdk",
                        "Ebs" : {
                            "VolumeSize": dataDiskSize,
                            "VolumeType": "gp2"
                        }
                    }
                ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": [ "", command]
                    }
                }
            }
        }
    }
    return resources

main()
