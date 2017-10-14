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

    serverVersion = parameters['serverVersion']
    syncGatewayVersion = parameters['syncGatewayVersion']
    cluster = parameters['cluster']

    template['Mappings'] = dict(template['Mappings'].items() + generateMappings(serverVersion, syncGatewayVersion).items())
    template['Resources'] = dict(template['Resources'].items() + generateMiscResources().items())
    template['Resources'] = dict(template['Resources'].items() + generateCluster(cluster).items())

    file = open('generated.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()

def generateMappings(serverVersion, syncGatewayVersion):
    allMappings = {
        "CouchbaseServer": {
            "4.6.2": {
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
            "4.6.3": {
                "us-east-1": { "BYOL": "ami-e14d569a", "HourlyPricing": "ami-e8405b93" },
                "us-east-2": { "BYOL": "ami-c83f1dad", "HourlyPricing": "ami-42391b27" },
                "us-west-1": { "BYOL": "ami-0ba4936b", "HourlyPricing": "ami-03a69163" },
                "us-west-2": { "BYOL": "ami-0426d77c", "HourlyPricing": "ami-0a2bda72" },
                "ca-central-1": { "BYOL": "ami-12d86176", "HourlyPricing": "ami-97e75ef3" },
                "eu-central-1": { "BYOL": "ami-17ae1978", "HourlyPricing": "ami-d5a116ba" },
                "eu-west-1": { "BYOL": "ami-da6faea3", "HourlyPricing": "ami-ab6cadd2" },
                "eu-west-2": { "BYOL": "ami-8a7f6cee", "HourlyPricing": "ami-e27f6c86" },
                "ap-southeast-1": { "BYOL": "ami-31a1ca52", "HourlyPricing": "ami-53a3c830" },
                "ap-southeast-2": { "BYOL": "ami-86ad4ae4", "HourlyPricing": "ami-3baa4d59" },
                "ap-south-1": { "BYOL": "ami-85aee9ea", "HourlyPricing": "ami-b0a1e6df" },
                "ap-northeast-1": { "BYOL": "ami-315c9c57", "HourlyPricing": "ami-905f9ff6" },
                "ap-northeast-2": { "BYOL": "ami-6bed3605", "HourlyPricing": "ami-6ded3603" },
                "sa-east-1": { "BYOL": "ami-ad9be9c1", "HourlyPricing": "ami-e29be98e" }
            },
            "5.0.0": {
                "us-east-1": { "BYOL": "ami-1642856c", "HourlyPricing": "ami-d64186ac" },
                "us-east-2": { "BYOL": "ami-17c3ee72", "HourlyPricing": "ami-30c0ed55" },
                "us-west-1": { "BYOL": "ami-2f41724f", "HourlyPricing": "ami-964675f6" },
                "us-west-2": { "BYOL": "ami-e5c6039d", "HourlyPricing": "ami-43c3063b" },
                "ca-central-1": { "BYOL": "ami-64259c00", "HourlyPricing": "ami-e9239a8d" },
                "eu-central-1": { "BYOL": "ami-979a27f8", "HourlyPricing": "ami-48942927" },
                "eu-west-1": { "BYOL": "ami-f99b4d80", "HourlyPricing": "ami-fb9b4d82" },
                "eu-west-2": { "BYOL": "ami-762f3d12", "HourlyPricing": "ami-3d2c3e59" },
                "ap-southeast-1": { "BYOL": "ami-1aed9279", "HourlyPricing": "ami-5eec933d" },
                "ap-southeast-2": { "BYOL": "ami-0adf3c68", "HourlyPricing": "ami-78de3d1a" },
                "ap-south-1": { "BYOL": "aami-934f0ffc", "HourlyPricing": "ami-7e4d0d11" },
                "ap-northeast-1": { "BYOL": "ami-8966b6ef", "HourlyPricing": "ami-0367b765" },
                "ap-northeast-2": { "BYOL": "ami-152df77b", "HourlyPricing": "ami-942ff5fa" },
                "sa-east-1": { "BYOL": "ami-b0a7d8dc", "HourlyPricing": "ami-87acd3eb" }
            }
        },
        "CouchbaseSyncGateway": {
            "1.4.1-3": {
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
            },
            "1.5.0": {
                "us-east-1": { "BYOL": "ami-4219d238", "HourlyPricing": "ami-611bd01b" },
                "us-east-2": { "BYOL": "ami-33456956", "HourlyPricing": "ami-aa4569cf" },
                "us-west-1": { "BYOL": "ami-b52715d5", "HourlyPricing": "ami-f5271595" },
                "us-west-2": { "BYOL": "ami-dfa263a7", "HourlyPricing": "ami-b79f5ecf" },
                "ca-central-1": { "BYOL": "ami-42ec5426", "HourlyPricing": "ami-43ec5427" },
                "eu-central-1": { "BYOL": "ami-c83a85a7", "HourlyPricing": "ami-843a85eb" },
                "eu-west-1": { "BYOL": "ami-306dbf49", "HourlyPricing": "ami-fa6dbf83" },
                "eu-west-2": { "BYOL": "ami-cca8baa8", "HourlyPricing": "ami-52a8ba36" },
                "ap-southeast-1": { "BYOL": "ami-47a6dd24", "HourlyPricing": "ami-faa4df99" },
                "ap-southeast-2": { "BYOL": "ami-cc40a2ae", "HourlyPricing": "ami-2d46a44f" },
                "ap-south-1": { "BYOL": "ami-a54506ca", "HourlyPricing": "ami-66450609" },
                "ap-northeast-1": { "BYOL": "ami-74c61812", "HourlyPricing": "ami-3fc81659" },
                "ap-northeast-2": { "BYOL": "ami-d4cd68ba", "HourlyPricing": "ami-1ecf6a70" },
                "sa-east-1": { "BYOL": "ami-42b3cd2e", "HourlyPricing": "ami-f1b0ce9d" }
            }
        }
    }
    mappings = {
        "CouchbaseServer": allMappings["CouchbaseServer"][serverVersion],
        "CouchbaseSyncGateway": allMappings["CouchbaseSyncGateway"][syncGatewayVersion]
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
