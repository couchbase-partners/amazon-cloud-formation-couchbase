import sys
import yaml
import json


def main():
    filename = sys.argv[1]

    print('Using parameter file: ' + filename)
    with open(filename, 'r')as stream:
        parameters = yaml.load(stream, Loader=yaml.FullLoader)
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

    template['Mappings'] = generateMappings()[0]
    # template['Mappings'] = dict(list(template['Mappings'].items()) + list(generateMappings().items()))
    template['Resources'] = dict(list(template['Resources'].items()) + list(generateMiscResources().items()))
    template['Resources'] = dict(
        list(template['Resources'].items()) + list(generateCluster(serverVersion, syncGatewayVersion, cluster).items()))

    file = open('generated.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()


def generateMappings():
    mappings = {
                   "CouchbaseServer": {
                       "ap-northeast-1": {
                           "BYOL": "ami-0362747692866cd8a",
                           "HourlyPricing": "ami-04fbb93f323b3ad84"
                       },
                       "ap-northeast-2": {
                           "BYOL": "ami-0b11f2e719e5fac01",
                           "HourlyPricing": "ami-0c8b7ee91124e9c2b"
                       },
                       "ap-south-1": {
                           "BYOL": "ami-0bc85af16671ebab4",
                           "HourlyPricing": "ami-065d1a1771bb3a897"
                       },
                       "ap-southeast-1": {
                           "BYOL": "ami-000a759f651573d50",
                           "HourlyPricing": "ami-0f6ac431d430acae3"
                       },
                       "ap-southeast-2": {
                           "BYOL": "ami-0590031abee3b5ee9",
                           "HourlyPricing": "ami-02e5a3ea4554a0295"
                       },
                       "ca-central-1": {
                           "BYOL": "ami-0968e6ac3942660d2",
                           "HourlyPricing": "ami-00cb21b9848e977a5"
                       },
                       "eu-central-1": {
                           "BYOL": "ami-0de4381810425485e",
                           "HourlyPricing": "ami-04552799870482af3"
                       },
                       "eu-west-1": {
                           "BYOL": "ami-02cbd84a01792bc76",
                           "HourlyPricing": "ami-04034e057050e1bb4"
                       },
                       "eu-west-2": {
                           "BYOL": "ami-010fa85c7b0152ec3",
                           "HourlyPricing": "ami-0ed864043543cfda8"
                       },
                       "eu-west-3": {
                           "BYOL": "ami-03bb90cb881172c51",
                           "HourlyPricing": "ami-0b7026377a8881250"
                       },
                       "sa-east-1": {
                           "BYOL": "ami-0b9ca2426910cf31b",
                           "HourlyPricing": "ami-060b577e8c0650f51"
                       },
                       "us-east-1": {
                           "BYOL": "ami-0621b9ba2b81e939c",
                           "HourlyPricing": "ami-0d3e108f16070ca60"
                       },
                       "us-east-2": {
                           "BYOL": "ami-0121b5e2357eb6e5e",
                           "HourlyPricing": "ami-095bc61014d727e46"
                       },
                       "us-west-1": {
                           "BYOL": "ami-0c411e6ff6bf7ff63",
                           "HourlyPricing": "ami-0a3256d4a344412bb"
                       },
                       "us-west-2": {
                           "BYOL": "ami-02c15e47d576743f8",
                           "HourlyPricing": "ami-015db11f95c164e13"
                       }
                   },
                   "CouchbaseSyncGateway": {
                       "ap-northeast-1": {
                           "BYOL": "ami-0d1faa24b7052bc9c",
                           "HourlyPricing": "ami-07d982ffa106f59a3"
                       },
                       "ap-northeast-2": {
                           "BYOL": "ami-054b045d2f4e6d048",
                           "HourlyPricing": "ami-0dae8c09074e87fee"
                       },
                       "ap-south-1": {
                           "BYOL": "ami-05b902554433cccb6",
                           "HourlyPricing": "ami-0c723d200acb42479"
                       },
                       "ap-southeast-1": {
                           "BYOL": "ami-0782763e8b5a7b08a",
                           "HourlyPricing": "ami-02212aa73bef0afe1"
                       },
                       "ap-southeast-2": {
                           "BYOL": "ami-02480d0f5c04f1843",
                           "HourlyPricing": "ami-0973f3b647f4820d7"
                       },
                       "ca-central-1": {
                           "BYOL": "ami-054166045356693aa",
                           "HourlyPricing": "ami-0f1d7ef2faed58108"
                       },
                       "eu-central-1": {
                           "BYOL": "ami-0ff950650c393fd0a",
                           "HourlyPricing": "ami-082ad5e996ab14c5e"
                       },
                       "eu-west-1": {
                           "BYOL": "ami-0c8f94b38e9787f7e",
                           "HourlyPricing": "ami-0bd743559d1ae9744"
                       },
                       "eu-west-2": {
                           "BYOL": "ami-0df44a7b664cf74b2",
                           "HourlyPricing": "ami-0a376fa1ef71f8305"
                       },
                       "eu-west-3": {
                           "BYOL": "ami-9e8d3de3",
                           "HourlyPricing": "ami-9f8d3de2"
                       },
                       "sa-east-1": {
                           "BYOL": "ami-08d5be9331edafa80",
                           "HourlyPricing": "ami-01f91e48086035565"
                       },
                       "us-east-1": {
                           "BYOL": "ami-037541b4c352434ff",
                           "HourlyPricing": "ami-09fdfb17cf362fc01"
                       },
                       "us-east-2": {
                           "BYOL": "ami-0e3daf71b6f23fd0e",
                           "HourlyPricing": "ami-09ae177b8bdddd332"
                       },
                       "us-west-1": {
                           "BYOL": "ami-0053cb76d843d8c71",
                           "HourlyPricing": "ami-0c43758f2a30dfec1"
                       },
                       "us-west-2": {
                           "BYOL": "ami-0931244a3a7e48b10",
                           "HourlyPricing": "ami-0decd93bea08de6fc"
                       }
                   }
               },
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
                                "autoscaling:DescribeTags",
                                "autoscaling:DescribeAutoScalingGroups",
                                "cloudformation:DescribeStackResources",
                                "cloudformation:DescribeStacks",
                                "autoscaling:DescribeAutoScalingInstances"
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
    # TODO: handle this better
    # temp change for version swapping
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
        "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
        "wget ${baseURL}server.sh\n",
        "wget ${baseURL}util.sh\n",
        "chmod +x *.sh\n",
    ]
    if groupName == rallyAutoScalingGroup:
        command.append("./server.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${serverVersion}\n")
    else:
        command.append("rallyAutoScalingGroup=")
        command.append({"Ref": rallyAutoScalingGroup + "AutoScalingGroup"})
        command.append("\n")
        command.append(
            "./server.sh " +
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
