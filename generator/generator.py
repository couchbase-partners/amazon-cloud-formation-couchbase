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
            },
            "License": {
              "Description": "License model can be BYOL or HourlyPricing",
              "Type": "String",
              "Default": "HourlyPricing"
            }
        },
        "Mappings": {},
        "Resources": {}
    }

    cluster = parameters['cluster']

    template['Mappings'] = dict(template['Mappings'].items() + generateMappings().items())
    template['Resources'] = dict(template['Resources'].items() + generateMiscResources().items())
    template['Resources'] = dict(template['Resources'].items() + generateCluster(cluster).items())

    file = open('generated.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()

def generateMappings():
    mappings = {
        "CouchbaseServer": {
            "us-east-1": { "BYOL": "ami-48f6d033", "HourlyPricing": "ami-d71f29c1" },
            "us-east-2": { "BYOL": "ami-2fe2c24a", "HourlyPricing": "ami-ef4f6e8a" },
            "us-west-1": { "BYOL": "ami-92a48cf2", "HourlyPricing": "ami-5c0a263c" },
            "us-west-2": { "BYOL": "ami-4ac92e32", "HourlyPricing": "ami-29fbec50" },
            "ca-central-1": { "BYOL": "ami-98ee50fc", "HourlyPricing": "ami-e2a91686" },
            "eu-central-1": { "BYOL": "ami-f761ce98", "HourlyPricing": "ami-5f2f8930" },
            "eu-west-1": { "BYOL": "ami-e4ee1a9d", "HourlyPricing": "ami-10b25769" },
            "eu-west-2": { "BYOL": "ami-c82736ac", "HourlyPricing": "ami-800315e4" },
            "ap-southeast-1": { "BYOL": "ami-536af530", "HourlyPricing": "ami-a048c6c3" },
            "ap-southeast-2": { "BYOL": "ami-4a948a29", "HourlyPricing": "ami-ba796ad9" },
            "ap-south-1": { "BYOL": "ami-87bdc6e8 ", "HourlyPricing": "ami-83700eec" },
            "ap-northeast-1": { "BYOL": "ami-07da3461", "HourlyPricing": "ami-910312f6" },
            "ap-northeast-2": { "BYOL": "ami-0de53c63", "HourlyPricing": "ami-553ae53b" },
            "sa-east-1": { "BYOL": "ami-301f695c", "HourlyPricing": "ami-6b107a07" }
        },
        "CouchbaseSyncGateway": {
            "us-east-1": { "BYOL": "ami-9cf7d1e7", "HourlyPricing": "ami-f80b3dee" },
            "us-east-2": { "BYOL": "ami-141f3f71", "HourlyPricing": "ami-fd4d6c98" },
            "us-west-1": { "BYOL": "ami-7ca58d1c", "HourlyPricing": "ami-910428f1" },
            "us-west-2": { "BYOL": "ami-57d6312f", "HourlyPricing": "ami-54e7f02d" },
            "ca-central-1": { "BYOL": "ami-23ed5347", "HourlyPricing": "ami-8ca718e8" },
            "eu-central-1": { "BYOL": "ami-fa62cd95", "HourlyPricing": "ami-b73492d8" },
            "eu-west-1": { "BYOL": "ami-20ee1a59", "HourlyPricing": "ami-95ba5fec" },
            "eu-west-2": { "BYOL": "ami-c12839a5", "HourlyPricing": "ami-b70214d3" },
            "ap-southeast-1": { "BYOL": "ami-206af543", "HourlyPricing": "ami-ba44cad9" },
            "ap-southeast-2": { "BYOL": "ami-00968863", "HourlyPricing": "ami-687f6c0b" },
            "ap-south-1": { "BYOL": "ami-5dbec532", "HourlyPricing": "ami-786e1017" },
            "ap-northeast-1": { "BYOL": "ami-e5df3183", "HourlyPricing": "ami-6d07160a" },
            "ap-northeast-2": { "BYOL": "ami-f6e23b98", "HourlyPricing": "ami-373be459" },
            "sa-east-1": { "BYOL": "ami-4d1e6821", "HourlyPricing": "ami-30167c5c" }
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

def generateCluster(cluster):
    resources = {}
    rallyAutoScalingGroup=cluster[0]['group']
    for group in cluster:
        groupResources=generateGroup(group, rallyAutoScalingGroup)
        resources = dict(resources.items() + groupResources.items())
    return resources

def generateGroup(group, rallyAutoScalingGroup):
    resources = {}
    if 'syncGateway' in group['services']:
        resources = dict(resources.items() + generateSyncGateway(group, rallyAutoScalingGroup).items())
    else:
        resources = dict(resources.items() + generateServer(group, rallyAutoScalingGroup).items())
    return resources

def generateSyncGateway(group, rallyAutoScalingGroup):
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
                "ImageId": { "Fn::FindInMap": [ "CouchbaseSyncGateway", { "Ref": "AWS::Region" }, { "Ref": "License" } ] },
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
                            "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
                            "wget ${baseURL}syncGateway.sh\n",
                            "chmod +x *.sh\n",
                            "./syncGateway.sh ${stackName}\n"
                        ]]
                    }
                }
            }
        }
    }
    return resources

def generateServer(group, rallyAutoScalingGroup):
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
        "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
        "wget ${baseURL}server.sh\n",
        "wget ${baseURL}util.sh\n",
        "chmod +x *.sh\n",
    ]
    if groupName==rallyAutoScalingGroup:
        command.append("./server.sh ${adminUsername} ${adminPassword} ${services} ${stackName}\n")
    else:
        command.append("rallyAutoScalingGroup=")
        command.append({ "Ref": rallyAutoScalingGroup + "AutoScalingGroup" })
        command.append("\n")
        command.append("./server.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${rallyAutoScalingGroup}\n")

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
                "ImageId": { "Fn::FindInMap": [ "CouchbaseServer", { "Ref": "AWS::Region" }, { "Ref": "License" } ] },
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
