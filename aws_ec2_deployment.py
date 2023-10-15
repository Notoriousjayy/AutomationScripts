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
print(f'Instance Public IP: {public_ip}')

# Run Ansible Playbook
ansible_command = f'ansible-playbook -i {public_ip}, {ANSIBLE_PLAYBOOK}'
os.system(ansible_command)
print('Ansible playbook executed successfully')

# Run Puppet Manifest
puppet_command = f'puppet apply {PUPPET_MANIFEST}'
subprocess.run(puppet_command, shell=True)
print('Puppet manifest applied successfully')

# Additional cleanup or post-deployment tasks can be added here

print('Deployment completed successfully')
