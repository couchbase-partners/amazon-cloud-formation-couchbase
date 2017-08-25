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
    }

    username = parameters['username']
    password = parameters['password']

    for cluster in parameters['clusters']:
        template['resources']+=generateCluster(cluster)

    file = open('generated.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()

def generateCluster(cluster):
    resources = []
    clusterName = cluster['cluster']
    region = cluster['region']
    for group in cluster['groups']:
        resources+=generateGroup(group)
    return resources

def generateGroup(group):
    groupName = group['group']
    nodeCount = group['nodeCount']
    nodeType = group['nodeType']
    diskSize = group['diskSize']
    services = group['services']

    resources={}
    return resources

main()
