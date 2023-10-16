import boto3

# Create a connection to AWS
session = boto3.Session()

# Get a list of all the processes in your account
ec2 = session.client('ec2')
processes = ec2.describe_processes()

# For each process, check if it is running
for process in processes['Processes']:
    if process['State'] == 'RUNNING':
        # Terminate the process
        ec2.terminate_processes(InstanceIds=[process['InstanceId']])
