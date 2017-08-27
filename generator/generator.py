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

    license = parameters['license']
    cluster = parameters['cluster']

    template['Mappings'] = dict(template['Mappings'].items() + generateMappings(license).items())
    template['Resources'] = dict(template['Resources'].items() + generateMiscResources().items())
    template['Resources'] = dict(template['Resources'].items() + generateCluster(cluster).items())

    file = open('generated.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()

def generateMappings(license):
    if license == 'byol':
        mappings = {
            "CouchbaseServerAMI": {
                "us-east-1": { "AMI": "ami-48f6d033" },
                "us-east-2": { "AMI": "ami-2fe2c24a" },
                "us-west-1": { "AMI": "ami-92a48cf2" },
                "us-west-2": { "AMI": "ami-4ac92e32" },
                "ca-central-1": { "AMI": "ami-98ee50fc" },
                "eu-central-1": { "AMI": "ami-f761ce98" },
                "eu-west-1": { "AMI": "ami-e4ee1a9d" },
                "eu-west-2": { "AMI": "ami-c82736ac" },
                "ap-southeast-1": { "AMI": "ami-536af530" },
                "ap-southeast-2": { "AMI": "ami-4a948a29" },
                "ap-south-1": { "AMI": "ami-87bdc6e8 " },
                "ap-northeast-1": { "AMI": "ami-07da3461" },
                "ap-northeast-2": { "AMI": "ami-0de53c63" },
                "sa-east-1": { "AMI": "ami-301f695c" }
            },
            "CouchbaseSyncGatewayAMI": {
                "us-east-1": { "AMI": "ami-9cf7d1e7" },
                "us-east-2": { "AMI": "ami-141f3f71" },
                "us-west-1": { "AMI": "ami-7ca58d1c" },
                "us-west-2": { "AMI": "ami-57d6312f" },
                "ca-central-1": { "AMI": "ami-23ed5347" },
                "eu-central-1": { "AMI": "ami-fa62cd95" },
                "eu-west-1": { "AMI": "ami-20ee1a59" },
                "eu-west-2": { "AMI": "ami-c12839a5" },
                "ap-southeast-1": { "AMI": "ami-206af543" },
                "ap-southeast-2": { "AMI": "ami-00968863" },
                "ap-south-1": { "AMI": "ami-5dbec532" },
                "ap-northeast-1": { "AMI": "ami-e5df3183" },
                "ap-northeast-2": { "AMI": "ami-f6e23b98" },
                "sa-east-1": { "AMI": "ami-4d1e6821" }
            }
        }
    else: # hourly-pricing
        mappings = {
            "CouchbaseServerAMI": {
              "us-east-1": { "AMI": "ami-d71f29c1" },
              "us-east-2": { "AMI": "ami-ef4f6e8a" },
              "us-west-1": { "AMI": "ami-5c0a263c" },
              "us-west-2": { "AMI": "ami-29fbec50" },
              "ca-central-1": { "AMI": "ami-e2a91686" },
              "eu-central-1": { "AMI": "ami-5f2f8930" },
              "eu-west-1": { "AMI": "ami-10b25769" },
              "eu-west-2": { "AMI": "ami-800315e4" },
              "ap-southeast-1": { "AMI": "ami-a048c6c3" },
              "ap-southeast-2": { "AMI": "ami-ba796ad9" },
              "ap-south-1": { "AMI": "ami-83700eec" },
              "ap-northeast-1": { "AMI": "ami-910312f6" },
              "ap-northeast-2": { "AMI": "ami-553ae53b" },
              "sa-east-1": { "AMI": "ami-6b107a07" }
            },
            "CouchbaseSyncGatewayAMI": {
                "us-east-1": { "AMI": "ami-f80b3dee" },
                "us-east-2": { "AMI": "ami-fd4d6c98" },
                "us-west-1": { "AMI": "ami-910428f1" },
                "us-west-2": { "AMI": "ami-54e7f02d" },
                "ca-central-1": { "AMI": "ami-8ca718e8" },
                "eu-central-1": { "AMI": "ami-b73492d8" },
                "eu-west-1": { "AMI": "ami-95ba5fec" },
                "eu-west-2": { "AMI": "ami-b70214d3" },
                "ap-southeast-1": { "AMI": "ami-ba44cad9" },
                "ap-southeast-2": { "AMI": "ami-687f6c0b" },
                "ap-south-1": { "AMI": "ami-786e1017" },
                "ap-northeast-1": { "AMI": "ami-6d07160a" },
                "ap-northeast-2": { "AMI": "ami-373be459" },
                "sa-east-1": { "AMI": "ami-30167c5c" }
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
    for group in cluster:
        resources = dict(resources.items() + generateGroup(group).items())
    return resources

def generateGroup(group):
    resources = {}
    if 'syncGateway' in group['services']:
        resources = dict(resources.items() + generateSyncGateway(group).items())
    else:
        resources = dict(resources.items() + generateServer(group).items())
    return resources

def generateSyncGateway(group):
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
                "ImageId": { "Fn::FindInMap": [ "CouchbaseSyncGatewayAMI", { "Ref": "AWS::Region" }, "AMI" ] },
                "InstanceType": nodeType,
                "SecurityGroups": [ { "Ref": "CouchbaseSecurityGroup" } ],
                "KeyName": { "Ref": "KeyName" },
                "EbsOptimized": True,
                "IamInstanceProfile": { "Ref": "CouchbaseInstanceProfile" },
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": [ "", [
                            "#!/bin/bash\n",
                            "echo 'Running startup script...'\n",
                            "stackName=", { "Ref": "AWS::StackName" }, "\n",
                            "rallyAutoScalingGroup=", { "Ref": "ServerAutoScalingGroup" }, "\n",
                            "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
                            "wget ${baseURL}syncGateway.sh\n",
                            "wget ${baseURL}configureSyncGateway.sh\n",
                            "wget ${baseURL}util.sh\n",
                            "chmod +x *.sh\n",
                            "./syncGateway.sh ${stackName} ${rallyAutoScalingGroup}\n"
                        ]]
                    }
                }
            }
        }
    }
    return resources

def generateServer(group):
    groupName = group['group']
    nodeCount = group['nodeCount']
    nodeType = group['nodeType']
    dataDiskSize = group['dataDiskSize']
    services = group['services']

    servicesParameter=''
    for service in services:
        servicesParameter += service + ','
    servicesParameter=servicesParameter[:-1]

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
                "ImageId": { "Fn::FindInMap": [ "CouchbaseServerAMI", { "Ref": "AWS::Region" }, "AMI" ] },
                "InstanceType": nodeType,
                "SecurityGroups": [ { "Ref": "CouchbaseSecurityGroup" } ],
                "KeyName": { "Ref": "KeyName" },
                "EbsOptimized": True,
                "IamInstanceProfile": { "Ref": "CouchbaseInstanceProfile" },
                "BlockDeviceMappings":
                [{
                    "DeviceName" : "/dev/sdk",
                    "Ebs" : {
                        "VolumeSize": dataDiskSize,
                        "VolumeType": "gp2"
                    }
                }],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": [ "", [
                            "#!/bin/bash\n",
                            "echo 'Running startup script...'\n",
                            "adminUsername=", { "Ref": "Username" }, "\n",
                            "adminPassword=", { "Ref": "Password" }, "\n",
                            "stackName=", { "Ref": "AWS::StackName" }, "\n",
                            "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
                            "wget ${baseURL}server.sh\n",
                            "wget ${baseURL}configureOS.sh\n",
                            "wget ${baseURL}format.sh\n",
                            "wget ${baseURL}configureServer.sh\n",
                            "wget ${baseURL}util.sh\n",
                            "chmod +x *.sh\n",
                            "./server.sh ${adminUsername} ${adminPassword} ${stackName}\n"
                        ]]
                    }
                }
            }
        }
    }
    return resources

main()
