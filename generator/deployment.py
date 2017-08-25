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
            "KeyName": {
                "Description": "Name of an existing EC2 KeyPair",
                "Type": "AWS::EC2::KeyPair::KeyName"
            }
        },
        "Mappings": {},
        "Resources": {}
    }

    license = parameters['license']
    username = parameters['username']
    password = parameters['password']
    cluster = parameters['cluster']

    template['Mappings'] = dict(template['Mappings'].items() + generateMappings(license).items())
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
    else:
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

def generateCluster(cluster):
    resources = {}
    for group in cluster:
        resources = dict(resources.items() + generateGroup(group).items())
    return resources

def generateGroup(group):
    groupName = group['group']
    nodeCount = group['nodeCount']
    nodeType = group['nodeType']
    diskSize = group['diskSize']
    services = group['services']

    resources = {}
    return resources

main()
