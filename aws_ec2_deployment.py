import boto3
import os
import subprocess

# AWS Configuration
AWS_REGION = 'YOUR_AWS_REGION'
AWS_INSTANCE_TYPE = 't2.micro'
AWS_IMAGE_ID = 'ami-xxxxxxxxxxxxxxxxx'  # Replace with your desired AMI ID
AWS_KEY_NAME = 'your-aws-key-name'
AWS_SECURITY_GROUP = ['your-security-group-id']

# Ansible Configuration
ANSIBLE_PLAYBOOK = 'YOUR_ANSIBLE_PLAYBOOK.yml'

# Puppet Configuration
PUPPET_MANIFEST = 'YOUR_PUPPET_MANIFEST.pp'

try:
    # AWS EC2 Instance Creation
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    response = ec2_client.run_instances(
        ImageId=AWS_IMAGE_ID,
        InstanceType=AWS_INSTANCE_TYPE,
        KeyName=AWS_KEY_NAME,
        SecurityGroupIds=AWS_SECURITY_GROUP,
        MinCount=1,
        MaxCount=1
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    print(f'Launched EC2 instance with ID: {instance_id}')
    
    # Wait for the instance to be running
    ec2_waiter = ec2_client.get_waiter('instance_running')
    ec2_waiter.wait(InstanceIds=[instance_id])
    print('Instance is running')
    
    # Get the public IP address of the instance
    instance = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    public_ip = instance.get('PublicIpAddress')
    if public_ip:
        print(f'Instance Public IP: {public_ip}')
    else:
        raise Exception('Failed to retrieve instance public IP address')
    
    # Run Ansible Playbook
    ansible_command = f'ansible-playbook -i {public_ip}, {ANSIBLE_PLAYBOOK}'
    ansible_result = subprocess.run(ansible_command, shell=True, capture_output=True)
    if ansible_result.returncode != 0:
        raise Exception(f'Ansible playbook execution failed: {ansible_result.stderr.decode()}')
    print('Ansible playbook executed successfully')
    
    # Run Puppet Manifest
    puppet_command = f'puppet apply {PUPPET_MANIFEST}'
    puppet_result = subprocess.run(puppet_command, shell=True, capture_output=True)
    if puppet_result.returncode != 0:
        raise Exception(f'Puppet manifest execution failed: {puppet_result.stderr.decode()}')
    print('Puppet manifest applied successfully')

    # Additional cleanup or post-deployment tasks can be added here

    print('Deployment completed successfully')

except Exception as e:
    print(f'Error: {str(e)}')
    # Handle the error, e.g., by sending notifications, rolling back changes, etc.
