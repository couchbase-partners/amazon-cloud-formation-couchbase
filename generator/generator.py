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
            "us-east-1": { "HourlyPricing": "ami-49e7e436", "BYOL": "ami-40dcdf3f", "PrivateHourlyPlat": "ami-0265a23a6b334304c", "PrivateHourlyGold": "ami-03577010f4a21dfc1", "PrivateBYOL": "ami-0f0cbdf64dac60912" },
            "us-east-2": { "HourlyPricing": "ami-17271d72", "BYOL": "ami-99271dfc", "PrivateHourlyPlat": "ami-03977a740555bf8ab", "PrivateHourlyGold": "ami-0aa9bc591250e6927", "PrivateBYOL": "ami-08b217b8db1bb14f3" },
            "us-west-1": { "HourlyPricing": "ami-edd03d8e", "BYOL": "ami-f5d13c96", "PrivateHourlyPlat": "ami-0f0ede7fd152a93e2", "PrivateHourlyGold": "ami-0fa8ad0dc9876b314", "PrivateBYOL": "ami-0fb65c398310a0736" },
            "us-west-2": { "HourlyPricing": "ami-53ce902b", "BYOL": "ami-70ca9408",  "PrivateHourlyPlat": "ami-0cb1125d99968b8df", "PrivateHourlyGold": "ami-079b12a3f3173c3f2", "PrivateBYOL": "ami-0ec331c14c38a4ae8" },
            "ca-central-1": { "HourlyPricing": "ami-acaa27c8", "BYOL": "ami-92911cf6", "PrivateHourlyPlat": "ami-0e044a4cec664dbfc", "PrivateHourlyGold": "ami-0b3d92624e06e92db", "PrivateBYOL": "ami-06aa8345e3431af5b" },
            "eu-central-1": { "HourlyPricing": "ami-3c7f7cd7", "BYOL": "ami-310201da", "PrivateHourlyPlat": "ami-06bf51c3bc7be03ff", "PrivateHourlyGold": "ami-07e63fc84e3cb0af3", "PrivateBYOL": "ami-0c13f646fa1825554" },
            "eu-west-1": { "HourlyPricing": "ami-3c7f64d6", "BYOL": "ami-3a7f64d0", "PrivateHourlyPlat": "ami-053d4f39839c01cbb", "PrivateHourlyGold": "ami-08b304d565d60788f", "PrivateBYOL": "ami-05ceb8de8f7e83c22" },
            "eu-west-2": { "HourlyPricing": "ami-48ea002f", "BYOL": "ami-69ed070e", "PrivateHourlyPlat": "ami-01e39d363307878ea", "PrivateHourlyGold": "ami-0209ce30de6035dd0", "PrivateBYOL": "ami-0aaaef8ceb67a1a8a" },
            "eu-west-3": { "HourlyPricing": "ami-718f3f0c", "BYOL": "ami-9d8d3de0", "PrivateHourlyPlat": "ami-04e5ae0c5576faaf2", "PrivateHourlyGold": "ami-089cce539024535e2", "PrivateBYOL": "ami-0e8607978d272c693" },
            "ap-southeast-1": { "HourlyPricing": "ami-ce7b3c24", "BYOL": "ami-8f85c265","PrivateHourlyPlat": "ami-0c015b73d118d05a3", "PrivateHourlyGold": "ami-06a0eab08bf25919e", "PrivateBYOL": "ami-0dd139097e52846a2" },
            "ap-southeast-2": { "HourlyPricing": "ami-cb298ea9", "BYOL": "ami-953394f7", "PrivateHourlyPlat": "ami-030ca7f3d0a4e9414", "PrivateHourlyGold": "ami-0ea48c87250b17e6f", "PrivateBYOL": "ami-02357aff956a327b2" },
            "ap-northeast-1": { "HourlyPricing": "ami-0f1f6ae2", "BYOL": "ami-220376cf", "PrivateHourlyPlat": "ami-04030f1c6aed4a066", "PrivateHourlyGold": "ami-0c0bc36ce1e451daf", "PrivateBYOL": "ami-09c8329c892efd3a4" },
            "ap-northeast-2": { "HourlyPricing": "ami-8f8b3ce1", "BYOL": "ami-b9893ed7", "PrivateHourlyPlat": "ami-03979fdd0236623c7", "PrivateHourlyGold": "ami-022649a13b10b33ac", "PrivateBYOL": "ami-007a1600d278ba81a" },
            "ap-south-1": { "HourlyPricing": "ami-4e8fbc21", "BYOL": "ami-658bb80a", "PrivateHourlyPlat": "ami-0964815bfdaa6777b", "PrivateHourlyGold": "ami-08209daec2fddc10e", "PrivateBYOL": "ami-074cec37a6eb7cf0d" },
            "sa-east-1": { "HourlyPricing": "ami-4151702d", "BYOL": "ami-3e290852", "PrivateHourlyPlat": "ami-0e5701affc2f066a2", "PrivateHourlyGold": "ami-0be2e1121d504b803", "PrivateBYOL": "ami-086794c41a1eb31b9" }
        },
        "CouchbaseSyncGateway": {
            "us-east-1": { "HourlyPricing": "ami-2ce5e653", "BYOL": "ami-f6e3e089", "PrivateHourlyPlat": "ami-0bb39f184d87a1a17", "PrivateHourlyGold": "ami-07913f4d354ecd472", "PrivateBYOL": "ami-0e703c6d1f3e6e249" },
            "us-east-2": { "HourlyPricing": "ami-bf251fda", "BYOL": "ami-10271d75", "PrivateHourlyPlat": "ami-039ac453fbac58d5d", "PrivateHourlyGold": "ami-01bdb4c377a24a53b", "PrivateBYOL": "ami-0bbb19a0c0de97823" },
            "us-west-1": { "HourlyPricing": "ami-cbd13ca8", "BYOL": "ami-f4d13c97", "PrivateHourlyPlat": "ami-0d2454b76648a4127", "PrivateHourlyGold": "ami-05587fe828189f355", "PrivateBYOL": "ami-052024155dc3f7155" },
            "us-west-2": { "HourlyPricing": "ami-ddcc92a5", "BYOL": "ami-dfcc92a7", "PrivateHourlyPlat": "ami-08df627e3135466da", "PrivateHourlyGold": "ami-093ff23c63a9c670c", "PrivateBYOL": "ami-016143aba59553fe5" },
            "ca-central-1": { "HourlyPricing": "ami-adaa27c9", "BYOL": "ami-13aa2777", "PrivateHourlyPlat": "ami-010d9004e963ea053", "PrivateHourlyGold": "ami-0c42c043171159bab", "PrivateBYOL": "ami-06f7563110ac99a4e" },
            "eu-central-1": { "HourlyPricing": "ami-3e7f7cd5", "BYOL": "ami-7e070495", "PrivateHourlyPlat": "ami-03e73d94cc8e3c657", "PrivateHourlyGold": "ami-0bb9acb88d567a1ec", "PrivateBYOL": "ami-076d4930127526263" },
            "eu-west-1": { "HourlyPricing": "ami-8a170c60", "BYOL": "ami-836a7169", "PrivateHourlyPlat": "ami-090053756a1cb9e3d", "PrivateHourlyGold": "ami-0fb8b03df4553d6ff", "PrivateBYOL": "ami-0a44b20a65c7ae3c4" },
            "eu-west-2": { "HourlyPricing": "ami-d3eb01b4", "BYOL": "ami-49ea002e", "PrivateHourlyPlat": "ami-0ac0cb9136be7092a", "PrivateHourlyGold": "ami-0ff4d2f16077fb9fd", "PrivateBYOL": "ami-0974d474cbefec841" },
            "eu-west-3": { "HourlyPricing": "ami-9f8d3de2", "BYOL": "ami-9e8d3de3", "PrivateHourlyPlat": "ami-034d54c2f686d384c", "PrivateHourlyGold": "ami-0bef1a36c3ac8d560", "PrivateBYOL": "ami-0bdb4dab356e43438" },
            "ap-southeast-1": { "HourlyPricing": "ami-0a783fe0", "BYOL": "ami-be7a3d54", "PrivateHourlyPlat": "ami-0d2a40fd679e1d368", "PrivateHourlyGold": "ami-082d6f57bb9227fb7", "PrivateBYOL": "ami-0d666045b0dc3afa2" },
            "ap-southeast-2": { "HourlyPricing": "ami-49288f2b", "BYOL": "ami-5833943a", "PrivateHourlyPlat": "ami-07f4a6a91413737ef", "PrivateHourlyGold": "ami-06bef34e9cfc712f1", "PrivateBYOL": "ami-0a390aa0802353893" },
            "ap-northeast-1": { "HourlyPricing": "ami-410b7eac", "BYOL": "ami-0b0174e6", "PrivateHourlyPlat": "ami-09943a2b5dd01e50d", "PrivateHourlyGold": "ami-0589e6f99c60e98dd", "PrivateBYOL": "ami-00142db2a4f18a091" },
            "ap-northeast-2": { "HourlyPricing": "ami-37823559", "BYOL": "ami-ca8631a4", "PrivateHourlyPlat": "ami-004cfbbd2265ea41a", "PrivateHourlyGold": "ami-0f12f12bd800f6562", "PrivateBYOL": "ami-0fc588e3c1d556971" },
            "ap-south-1": { "HourlyPricing": "ami-4174462e", "BYOL": "ami-628bb80d", "PrivateHourlyPlat": "ami-0d7e5b8ef15e1635d", "PrivateHourlyGold": "ami-0e0ea2f0a58a01d98", "PrivateBYOL": "ami-0f2fe809a9abece67" },
            "sa-east-1": { "HourlyPricing": "ami-457a5b29", "BYOL": "ami-14577678", "PrivateHourlyPlat": "ami-036c3f608a9d55f93", "PrivateHourlyGold": "ami-0fd589dc9ec12fb5b", "PrivateBYOL": "ami-021dec08d0008bb83" }
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
                "MinSize": 0,
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
                            "VolumeType": "gp2",
                            "Encrypted": True
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
