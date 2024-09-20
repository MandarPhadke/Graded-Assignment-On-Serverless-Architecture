import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    stopInstances()
    startInstances()

def stopInstances():
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:MandarDevOps',
                'Values': ['Auto-Stop']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    
    instances_to_stop = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])
    
    if instances_to_stop:
        print(f"Stopping instances: {instances_to_stop}")
        ec2.stop_instances(InstanceIds=instances_to_stop)
    else:
        print("No instances found with the 'Auto-Stop' tag that are running.")

def startInstances():
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:MandarDevOps',
                'Values': ['Auto-Start']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }
        ]
    )
    
    instances_to_start = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_start.append(instance['InstanceId'])
    
    if instances_to_start:
        print(f"Starting instances: {instances_to_start}")
        ec2.start_instances(InstanceIds=instances_to_start)
    else:
        print("No instances found with the 'Auto-Start' tag that are stopped.")
