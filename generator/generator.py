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
            "us-east-1": { "HourlyPricing": "ami-49e7e436", "BYOL": "ami-40dcdf3f" },
            "us-east-2": { "HourlyPricing": "ami-17271d72", "BYOL": "ami-99271dfc" },
            "us-west-1": { "HourlyPricing": "ami-edd03d8e", "BYOL": "ami-f5d13c96" },
            "us-west-2": { "HourlyPricing": "ami-53ce902b", "BYOL": "ami-70ca9408" },
            "ca-central-1": { "HourlyPricing": "ami-acaa27c8", "BYOL": "ami-92911cf6" },
            "eu-central-1": { "HourlyPricing": "ami-3c7f7cd7", "BYOL": "ami-310201da" },
            "eu-west-1": { "HourlyPricing": "ami-3c7f64d6", "BYOL": "ami-3a7f64d0" },
            "eu-west-2": { "HourlyPricing": "ami-48ea002f", "BYOL": "ami-69ed070e" },
            "eu-west-3": { "HourlyPricing": "ami-718f3f0c", "BYOL": "ami-9d8d3de0"},
            "ap-southeast-1": { "HourlyPricing": "ami-ce7b3c24", "BYOL": "ami-8f85c265"},
            "ap-southeast-2": { "HourlyPricing": "ami-cb298ea9", "BYOL": "ami-953394f7"},
            "ap-northeast-1": { "HourlyPricing": "ami-0f1f6ae2", "BYOL": "ami-220376cf" },
            "ap-northeast-2": { "HourlyPricing": "ami-8f8b3ce1", "BYOL": "ami-b9893ed7" },
            "ap-south-1": { "HourlyPricing": "ami-4e8fbc21", "BYOL": "ami-658bb80a" },
            "sa-east-1": { "HourlyPricing": "ami-4151702d", "BYOL": "ami-3e290852" }
        },
        "CouchbaseSyncGateway": {
            "us-east-1": { "HourlyPricing": "ami-2ce5e653", "BYOL": "ami-f6e3e089" },
            "us-east-2": { "HourlyPricing": "ami-bf251fda", "BYOL": "ami-10271d75" },
            "us-west-1": { "HourlyPricing": "ami-cbd13ca8", "BYOL": "ami-f4d13c97" },
            "us-west-2": { "HourlyPricing": "ami-ddcc92a5", "BYOL": "ami-dfcc92a7" },
            "ca-central-1": { "HourlyPricing": "ami-adaa27c9", "BYOL": "ami-13aa2777" },
            "eu-central-1": { "HourlyPricing": "ami-3e7f7cd5", "BYOL": "ami-7e070495" },
            "eu-west-1": { "HourlyPricing": "ami-8a170c60", "BYOL": "ami-836a7169" },
            "eu-west-2": { "HourlyPricing": "ami-d3eb01b4", "BYOL": "ami-49ea002e" },
            "eu-west-3": { "HourlyPricing": "ami-9f8d3de2", "BYOL": "ami-9e8d3de3" },
            "ap-southeast-1": { "HourlyPricing": "ami-0a783fe0", "BYOL": "ami-be7a3d54" },
            "ap-southeast-2": { "HourlyPricing": "ami-49288f2b", "BYOL": "ami-5833943a" },
            "ap-northeast-1": { "HourlyPricing": "ami-410b7eac", "BYOL": "ami-0b0174e6" },
            "ap-northeast-2": { "HourlyPricing": "ami-37823559", "BYOL": "ami-ca8631a4" },
            "ap-south-1": { "HourlyPricing": "ami-4174462e", "BYOL": "ami-628bb80d" },
            "sa-east-1": { "HourlyPricing": "ami-457a5b29", "BYOL": "ami-14577678" }
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
                "ImageId": { "Fn::FindInMap": [ "CouchbaseSyncGateway", { "Ref": "AWS::Region" }, license ] },
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
                            "syncGatewayVersion=" + syncGatewayVersion + "\n",
                            "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
                            "wget ${baseURL}syncGateway.sh\n",
                            "chmod +x *.sh\n",
                            "./syncGateway.sh ${stackName} ${syncGatewayVersion}\n"
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
        "serverVersion=" + serverVersion + "\n",
        "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
        "wget ${baseURL}server.sh\n",
        "wget ${baseURL}util.sh\n",
        "chmod +x *.sh\n",
    ]
    if groupName==rallyAutoScalingGroup:
        command.append("./server.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${serverVersion}\n")
    else:
        command.append("rallyAutoScalingGroup=")
        command.append({ "Ref": rallyAutoScalingGroup + "AutoScalingGroup" })
        command.append("\n")
        command.append("./server.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${serverVersion} ${rallyAutoScalingGroup}\n")

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
                "ImageId": { "Fn::FindInMap": [ "CouchbaseServer", { "Ref": "AWS::Region" }, license ] },
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
