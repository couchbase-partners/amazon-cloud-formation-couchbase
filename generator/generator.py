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
    license = parameters['license']
    cluster = parameters['cluster']

    template['Mappings'] = dict(template['Mappings'].items() + generateMappings(license, serverVersion, syncGatewayVersion).items())
    template['Resources'] = dict(template['Resources'].items() + generateMiscResources().items())
    template['Resources'] = dict(template['Resources'].items() + generateCluster(license, serverVersion, syncGatewayVersion, cluster).items())

    file = open('generated.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()

def generateMappings(license, serverVersion, syncGatewayVersion):
    allMappings = {
        "AmazonLinux": {
                "2017.09.1.20180307": {
                "us-east-1": { "AMI": "ami-1853ac65" },
                "us-east-2": { "AMI": "ami-25615740" },
                "us-west-1": { "AMI": "ami-bf5540df" },
                "us-west-2": { "AMI": "ami-d874e0a0" },
                "ca-central-1": { "AMI": "ami-5b55d23f" },
                "eu-central-1": { "AMI": "ami-ac442ac3" },
                "eu-west-1": { "AMI": "ami-3bfab942" },
                "eu-west-2": { "AMI": "ami-dff017b8" },
                "eu-west-3": { "AMI": "ami-4f55e332" },
                "ap-southeast-1": { "AMI": "ami-e2adf99e" },
                "ap-southeast-2": { "AMI": "ami-43874721" },
                "ap-northeast-1": { "AMI": "ami-a77c30c1" },
                "ap-northeast-2": { "AMI": "ami-5e1ab730" },
                "ap-south-1": { "AMI": "ami-7c87d913" },
                "sa-east-1": { "AMI": "ami-5339733f" },
                "us-gov-west-1": { "AMI": "ami-2b39b24a" }
            }
        },
        "CouchbaseServer": {
            "4.6.4": {
                "us-east-1": { "BYOL": "ami-63af9f19", "HourlyPricing": "ami-279faf5d" },
                "us-east-2": { "BYOL": "ami-d17742b4", "HourlyPricing": "ami-f4704591" },
                "us-west-1": { "BYOL": "ami-018d8061", "HourlyPricing": "ami-b88d80d8" },
                "us-west-2": { "BYOL": "ami-eea11e96", "HourlyPricing": "ami-b99728c1" },
                "ca-central-1": { "BYOL": "ami-4723a623", "HourlyPricing": "ami-492ca92d" },
                "eu-central-1": { "BYOL": "ami-82079eed", "HourlyPricing": "ami-d63ca5b9" },
                "eu-west-1": { "BYOL": "ami-1c88ef65", "HourlyPricing": "ami-fc99fe85" },
                "eu-west-2": { "BYOL": "ami-12445e76", "HourlyPricing": "ami-cb455faf" },
                "eu-west-3": { "BYOL": "ami-86d96ffb", "HourlyPricing": "ami-d3dd6bae" },
                "ap-southeast-1": { "BYOL": "ami-6fed9513", "HourlyPricing": "ami-17ed956b" },
                "ap-southeast-2": { "BYOL": "ami-3b0ef059", "HourlyPricing": "ami-c30ef0a1" },
                "ap-northeast-1": { "BYOL": "ami-1eea8778", "HourlyPricing": "ami-75e78a13" },
                "ap-northeast-2": { "BYOL": "ami-b19330df", "HourlyPricing": "ami-888e2de6" },
                "ap-south-1": { "BYOL": "ami-83b1e0ec", "HourlyPricing": "ami-c8b0e1a7" },
                "sa-east-1": { "BYOL": "ami-f4551998", "HourlyPricing": "ami-d3571bbf" }
            },
            "5.0.1": {
                "us-east-1": { "BYOL": "ami-a693a3dc", "HourlyPricing": "ami-ef95a595" },
                "us-east-2": { "BYOL": "ami-d97441bc", "HourlyPricing": "ami-62764307" },
                "us-west-1": { "BYOL": "ami-cf8c81af", "HourlyPricing": "ami-c08c81a0" },
                "us-west-2": { "BYOL": "ami-269c235e", "HourlyPricing": "ami-49a11e31" },
                "ca-central-1": { "BYOL": "ami-9822a7fc", "HourlyPricing": "ami-2e22a74a" },
                "eu-central-1": { "BYOL": "ami-8438a1eb", "HourlyPricing": "ami-9939a0f6" },
                "eu-west-1": { "BYOL": "ami-078aed7e", "HourlyPricing": "ami-7797f00e" },
                "eu-west-2": { "BYOL": "ami-dd455fb9", "HourlyPricing": "ami-be7b61da" },
                "eu-west-3": { "BYOL": "ami-d5dd6ba8", "HourlyPricing": "ami-5bc77126" },
                "ap-southeast-1": { "BYOL": "ami-33ec944f", "HourlyPricing": "ami-13eb936f" },
                "ap-southeast-2": { "BYOL": "ami-8910eeeb", "HourlyPricing": "ami-ec11ef8e" },
                "ap-northeast-1": { "BYOL": "ami-b0e489d6", "HourlyPricing": "ami-47e48921" },
                "ap-northeast-2": { "BYOL": "ami-ec8d2e82", "HourlyPricing": "ami-e78c2f89" },
                "ap-south-1": { "BYOL": "aami-0d8ddc62", "HourlyPricing": "ami-5db1e032" },
                "sa-east-1": { "BYOL": "ami-995519f5", "HourlyPricing": "ami-f5551999" }
            },
            "5.1.0": {
                "us-east-1": { "BYOL": "ami-33ea154e", "HourlyPricing": "ami-aeef10d3" },
                "us-east-2": { "BYOL": "ami-a26751c7", "HourlyPricing": "ami-866650e3" },
                "us-west-1": { "BYOL": "ami-12a5af72", "HourlyPricing": "ami-d0bab0b0" },
                "us-west-2": { "BYOL": "ami-5fbb2f27", "HourlyPricing": "ami-acb92dd4" },
                "ca-central-1": { "BYOL": "ami-7754d313", "HourlyPricing": "ami-9c57d0f8" },
                "eu-central-1": { "BYOL": "ami-76670919", "HourlyPricing": "ami-57640a38" },
                "eu-west-1": { "BYOL": "ami-d7b4f7ae", "HourlyPricing": "ami-f1b6f588" },
                "eu-west-2": { "BYOL": "ami-30e80f57", "HourlyPricing": "ami-cff710a8" },
                "eu-west-3": { "BYOL": "ami-8954e2f4", "HourlyPricing": "ami-8854e2f5" },
                "ap-southeast-1": { "BYOL": "ami-4f8dd933", "HourlyPricing": "ami-7b8cd807" },
                "ap-southeast-2": { "BYOL": "ami-f975b49b", "HourlyPricing": "ami-fa75b498" },
                "ap-northeast-1": { "BYOL": "ami-fa430f9c", "HourlyPricing": "ami-92410df4" },
                "ap-northeast-2": { "BYOL": "ami-ec1eb382", "HourlyPricing": "ami-8a1fb2e4" },
                "ap-south-1": { "BYOL": "ami-8f90cee0", "HourlyPricing": "ami-c690cea9" },
                "sa-east-1": { "BYOL": "ami-a42963c8", "HourlyPricing": "ami-a72963cb" }
            }
        },
        "CouchbaseSyncGateway": {
            "1.5.1": {
                "us-east-1": { "BYOL": "ami-8294a4f8", "HourlyPricing": "ami-6d93a317" },
                "us-east-2": { "BYOL": "ami-0877426d", "HourlyPricing": "ami-0f75406a" },
                "us-west-1": { "BYOL": "ami-288c8148", "HourlyPricing": "ami-76f2ff16" },
                "us-west-2": { "BYOL": "ami-589c2320", "HourlyPricing": "ami-41a01f39" },
                "ca-central-1": { "BYOL": "ami-ad20a5c9", "HourlyPricing": "ami-c22da8a6" },
                "eu-central-1": { "BYOL": "ami-103aa37f", "HourlyPricing": "ami-d5069fba" },
                "eu-west-1": { "BYOL": "ami-b696f1cf", "HourlyPricing": "ami-c293f4bb" },
                "eu-west-2": { "BYOL": "ami-6c445e08", "HourlyPricing": "ami-11445e75" },
                "eu-west-3": { "BYOL": "ami-c9d86eb4", "HourlyPricing": "ami-58c77125" },
                "ap-southeast-1": { "BYOL": "ami-10eb936c", "HourlyPricing": "ami-a4ed95d8" },
                "ap-southeast-2": { "BYOL": "ami-a610eec4", "HourlyPricing": "ami-2911ef4b" },
                "ap-northeast-1": { "BYOL": "ami-b9e588df", "HourlyPricing": "ami-b3e588d5" },
                "ap-northeast-2": { "BYOL": "ami-38933056", "HourlyPricing": "ami-648c2f0a" },
                "ap-south-1": { "BYOL": "ami-898cdde6", "HourlyPricing": "ami-058cdd6a" },
                "sa-east-1": { "BYOL": "ami-3654185a", "HourlyPricing": "ami-b95a16d5" }
            }
        }
    }
    if license=="NULL":
        mappings = {
            "CouchbaseServer": allMappings["AmazonLinux"]["2017.09.1.20180307"],
            "CouchbaseSyncGateway": allMappings["AmazonLinux"]["2017.09.1.20180307"]
        }
    else:
        mappings={
            "CouchbaseServer": {},
            "CouchbaseSyncGateway": {}
        }
        for region in allMappings["CouchbaseServer"][serverVersion]:
            mappings["CouchbaseServer"][region]={}
            mappings["CouchbaseServer"][region]["AMI"]=allMappings["CouchbaseServer"][serverVersion][region][license]
        for region in allMappings["CouchbaseSyncGateway"][syncGatewayVersion]:
            mappings["CouchbaseSyncGateway"][region]={}
            mappings["CouchbaseSyncGateway"][region]["AMI"]=allMappings["CouchbaseSyncGateway"][syncGatewayVersion][region][license]
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
                    { "IpProtocol": "tcp", "FromPort": 8091, "ToPort": 8094, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 9100, "ToPort": 9105, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 9998, "ToPort": 9999, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 11207, "ToPort": 11215, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 18091, "ToPort": 18093, "CidrIp": "0.0.0.0/0" },
                    { "IpProtocol": "tcp", "FromPort": 21100, "ToPort": 21299, "CidrIp": "0.0.0.0/0" }
                ]
            }
        }
    }
    return resources

def generateCluster(license, serverVersion, syncGatewayVersion, cluster):
    resources = {}
    rallyAutoScalingGroup=cluster[0]['group']
    for group in cluster:
        groupResources=generateGroup(license, serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup)
        resources = dict(resources.items() + groupResources.items())
    return resources

def generateGroup(license, serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup):
    resources = {}
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
