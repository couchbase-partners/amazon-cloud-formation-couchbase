import sys
import yaml
import json


def main():
    filename = sys.argv[1]


    print('Using parameter file: ' + filename)
    with open(filename, 'r')as stream:
        parameters = yaml.load(stream)
    print('Parameters: ' + str(parameters))

    template = {
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

    template['Mappings'] = dict(list(template['Mappings'].items()) + list(generateMappings().items()))
    template['Resources'] = dict(list(template['Resources'].items()) + list(generateMiscResources().items()))
    template['Resources'] = dict(
        list(template['Resources'].items()) + list(generateCluster(serverVersion, syncGatewayVersion, cluster).items()))

    file = open('generated_beta.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()


def generateMappings():
    mappings = {
        "CouchbaseServer": {
            "ap-northeast-1": {
                "BYOL": "ami-220376cf",
                "BYOL6": "ami-0043e21657273c381",
                "HourlyPricing": "ami-0f1f6ae2",
                "HourlyPricing6": "ami-025cacffb6956de83"
            },
            "ap-northeast-2": {
                "BYOL": "ami-b9893ed7",
                "BYOL6": "ami-0ac6bc3976160e676",
                "HourlyPricing": "ami-8f8b3ce1",
                "HourlyPricing6": "ami-04cd85d7ce059f44d"
            },
            "ap-south-1": {
                "BYOL": "ami-658bb80a",
                "BYOL6": "ami-026c31b67560d4423",
                "HourlyPricing": "ami-4e8fbc21",
                "HourlyPricing6": "ami-02c0ed47fb3bacd5e"
            },
            "ap-southeast-1": {
                "BYOL": "ami-8f85c265",
                "BYOL6": "ami-06742e5872951238f",
                "HourlyPricing": "ami-ce7b3c24",
                "HourlyPricing6": "ami-09d5d25ccfd775e12"
            },
            "ap-southeast-2": {
                "BYOL": "ami-953394f7",
                "BYOL6": "ami-028010ed2755736b1",
                "HourlyPricing": "ami-cb298ea9",
                "HourlyPricing6": "ami-084f40f9b280c4d01"
            },
            "ca-central-1": {
                "BYOL": "ami-92911cf6",
                "BYOL6": "ami-0fb33bc84edd8a57b",
                "HourlyPricing": "ami-acaa27c8",
                "HourlyPricing6": "ami-04dc948ffb33fc3f5"
            },
            "eu-central-1": {
                "BYOL": "ami-310201da",
                "BYOL6": "ami-03b9f7be7aeaf970b",
                "HourlyPricing": "ami-3c7f7cd7",
                "HourlyPricing6": "ami-0d65603f43184c532"
            },
            "eu-west-1": {
                "BYOL": "ami-3a7f64d0",
                "BYOL6": "ami-05540fc6076bd0cb0",
                "HourlyPricing": "ami-3c7f64d6",
                "HourlyPricing6": "ami-0a7eb55ee6908d2f5"
            },
            "eu-west-2": {
                "BYOL": "ami-69ed070e",
                "BYOL6": "ami-0d9f2cbb1ce8ef0d7",
                "HourlyPricing": "ami-48ea002f",
                "HourlyPricing6": "ami-0c86641f9a20d33d3"
            },
            "eu-west-3": {
                "BYOL": "ami-9d8d3de0",
                "BYOL6": "ami-03bb90cb881172c51",
                "HourlyPricing": "ami-718f3f0c",
                "HourlyPricing6": "ami-0b7026377a8881250"
            },
            "sa-east-1": {
                "BYOL": "ami-3e290852",
                "BYOL6": "ami-0c6ca2d19baa7133c",
                "HourlyPricing": "ami-4151702d",
                "HourlyPricing6": "ami-024ff8c5608dc8445"
            },
            "us-east-1": {
                "BYOL": "ami-40dcdf3f",
                "BYOL6": "ami-04325927bb7941774",
                "HourlyPricing": "ami-49e7e436",
                "HourlyPricing6": "ami-0eabe2d728d85bec8"
            },
            "us-east-2": {
                "BYOL": "ami-99271dfc",
                "BYOL6": "ami-0f299d4b42ca0c09e",
                "HourlyPricing": "ami-17271d72",
                "HourlyPricing6": "ami-09078b360366c35bc"
            },
            "us-west-1": {
                "BYOL": "ami-f5d13c96",
                "BYOL6": "ami-07af8cdb76dcd41b5",
                "HourlyPricing": "ami-edd03d8e",
                "HourlyPricing6": "ami-0498c7038ee513a92"
            },
            "us-west-2": {
                "BYOL": "ami-70ca9408",
                "BYOL6": "ami-045f624d6ab821556",
                "HourlyPricing": "ami-53ce902b",
                "HourlyPricing6": "ami-09afb2a27d62d6073"
            }
        },
        "CouchbaseSyncGateway": {
            "ap-northeast-1": {
                "BYOL": "ami-0b0174e6",
                "HourlyPricing": "ami-410b7eac"
            },
            "ap-northeast-2": {
                "BYOL": "ami-ca8631a4",
                "HourlyPricing": "ami-37823559"
            },
            "ap-south-1": {
                "BYOL": "ami-628bb80d",
                "HourlyPricing": "ami-4174462e"
            },
            "ap-southeast-1": {
                "BYOL": "ami-be7a3d54",
                "HourlyPricing": "ami-0a783fe0"
            },
            "ap-southeast-2": {
                "BYOL": "ami-5833943a",
                "HourlyPricing": "ami-49288f2b"
            },
            "ca-central-1": {
                "BYOL": "ami-13aa2777",
                "HourlyPricing": "ami-adaa27c9"
            },
            "eu-central-1": {
                "BYOL": "ami-7e070495",
                "HourlyPricing": "ami-3e7f7cd5"
            },
            "eu-west-1": {
                "BYOL": "ami-836a7169",
                "HourlyPricing": "ami-8a170c60"
            },
            "eu-west-2": {
                "BYOL": "ami-49ea002e",
                "HourlyPricing": "ami-d3eb01b4"
            },
            "eu-west-3": {
                "BYOL": "ami-9e8d3de3",
                "HourlyPricing": "ami-9f8d3de2"
            },
            "sa-east-1": {
                "BYOL": "ami-14577678",
                "HourlyPricing": "ami-457a5b29"
            },
            "us-east-1": {
                "BYOL": "ami-f6e3e089",
                "HourlyPricing": "ami-2ce5e653"
            },
            "us-east-2": {
                "BYOL": "ami-10271d75",
                "HourlyPricing": "ami-bf251fda"
            },
            "us-west-1": {
                "BYOL": "ami-f4d13c97",
                "HourlyPricing": "ami-cbd13ca8"
            },
            "us-west-2": {
                "BYOL": "ami-dfcc92a7",
                "HourlyPricing": "ami-ddcc92a5"
            }
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
                "GroupDescription": "Enable SSH and Couchbase Ports",
                "SecurityGroupIngress": [{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 4369, "ToPort": 4369, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 4984, "ToPort": 4985, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 8091, "ToPort": 8096, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 9100, "ToPort": 9105, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 9110, "ToPort": 9122, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 9998, "ToPort": 9999, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 11207, "ToPort": 11215,
                                          "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 18091, "ToPort": 18096,
                                          "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 21100, "ToPort": 21299,
                                          "CidrIp": "0.0.0.0/0"}
                                         ]
            }
        }
    }


    return resources


def generateCluster(serverVersion, syncGatewayVersion, cluster):
    resources = {}


    rallyAutoScalingGroup = cluster[0]['group']
    for group in cluster:
        groupResources = generateGroup(serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup)
        resources = dict(list(resources.items()) + list(groupResources.items()))
    return resources


def generateGroup(serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup):
    resources = {}


    license = group['license']
    if 'syncGateway' in group['services']:
        resources = dict(
            list(resources.items()) + list(generateSyncGateway(license, syncGatewayVersion, group, rallyAutoScalingGroup).items()))
    else:
        resources = dict(list(resources.items()) + list(generateServer(license, serverVersion, group, rallyAutoScalingGroup).items()))
    return resources


def generateSyncGateway(license, syncGatewayVersion, group, rallyAutoScalingGroup):
    groupName = group['group']
    nodeCount = group['nodeCount']
    nodeType = group['nodeType']
    #TODO: handle this better
    #temp change for version swapping
    if license == 'BYOL6':
        license == 'BYOL'

    resources = {
        groupName + "AutoScalingGroup": {
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "AvailabilityZones": {"Fn::GetAZs": ""},
                "LaunchConfigurationName": {"Ref": groupName + "LaunchConfiguration"},
                "MinSize": 0,
                "MaxSize": 100,
                "DesiredCapacity": nodeCount
            }
        },
        groupName + "LaunchConfiguration": {
            "Type": "AWS::AutoScaling::LaunchConfiguration",
            "Properties": {
                "ImageId": {"Fn::FindInMap": ["CouchbaseSyncGateway", {"Ref": "AWS::Region"}, license]},
                "InstanceType": nodeType,
                "SecurityGroups": [{"Ref": "CouchbaseSecurityGroup"}],
                "KeyName": {"Ref": "KeyName"},
                "EbsOptimized": True,
                "IamInstanceProfile": {"Ref": "CouchbaseInstanceProfile"},
                "BlockDeviceMappings":
                    [{
                        "DeviceName": "/dev/xvda",
                        "Ebs": {"DeleteOnTermination": True}
                    }
                    ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": ["", [
                            "#!/bin/bash\n",
                            "echo 'Running startup script...'\n",
                            "stackName=", {"Ref": "AWS::StackName"}, "\n",
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

    servicesParameter = ''
    for service in services:
        servicesParameter += service + ','
    servicesParameter = servicesParameter[:-1]

    command = [
        "#!/bin/bash\n",
        "echo 'Running startup script...'\n",
        "adminUsername=", {"Ref": "Username"}, "\n",
        "adminPassword=", {"Ref": "Password"}, "\n",
        "services=" + servicesParameter + "\n",
        "stackName=", {"Ref": "AWS::StackName"}, "\n",
        "serverVersion=" + serverVersion + "\n",
        "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/6.5Test/scripts/\n",
        "wget ${baseURL}server_beta.sh\n",
        "wget ${baseURL}utilAmzLnx2.sh\n",
        "chmod +x *.sh\n",
    ]
    if groupName == rallyAutoScalingGroup:
        command.append("./server_beta.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${serverVersion}\n")
    else:
        command.append("rallyAutoScalingGroup=")
        command.append({"Ref": rallyAutoScalingGroup + "AutoScalingGroup"})
        command.append("\n")
        command.append(
            "./server_beta.sh " +
            "${adminUsername} ${adminPassword} ${services} ${stackName} ${serverVersion} ${rallyAutoScalingGroup}\n")

    resources = {
        groupName + "AutoScalingGroup": {
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "AvailabilityZones": {"Fn::GetAZs": ""},
                "LaunchConfigurationName": {"Ref": groupName + "LaunchConfiguration"},
                "MinSize": 0,
                "MaxSize": 100,
                "DesiredCapacity": nodeCount
            }
        },
        groupName + "LaunchConfiguration": {
            "Type": "AWS::AutoScaling::LaunchConfiguration",
            "Properties": {
                "ImageId": {"Fn::FindInMap": ["CouchbaseServer", {"Ref": "AWS::Region"}, license]},
                "InstanceType": nodeType,
                "SecurityGroups": [{"Ref": "CouchbaseSecurityGroup"}],
                "KeyName": {"Ref": "KeyName"},
                "EbsOptimized": True,
                "IamInstanceProfile": {"Ref": "CouchbaseInstanceProfile"},
                "BlockDeviceMappings":
                    [{
                        "DeviceName": "/dev/xvda",
                        "Ebs": {"DeleteOnTermination": True}
                    }, {
                        "DeviceName": "/dev/sdk",
                        "Ebs": {
                            "VolumeSize": dataDiskSize,
                            "VolumeType": "gp2",
                            "Encrypted": True
                        }
                    }
                    ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": ["", command]
                    }
                }
            }
        }
    }
    return resources

main()
