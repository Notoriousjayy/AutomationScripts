import boto3
import subprocess
import os
import time

# AWS Configuration
aws_region = "your-aws-region"
aws_access_key_id = "your-access-key-id"
aws_secret_access_key = "your-secret-access-key"

# ECR Configuration
ecr_repository_name = "your-ecr-repo-name"

# Kubernetes Configuration
eks_cluster_name = "your-eks-cluster-name"
k8s_manifest_file = "path/to/your/k8s-manifest.yaml"

# Initialize AWS SDK (Boto3)
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

ecr_client = session.client('ecr')
eks_client = session.client('eks')

# Step 1: Create an ECR Repository
def create_ecr_repository(repo_name):
    response = ecr_client.create_repository(
        repositoryName=repo_name
    )
    return response['repository']

# Step 2: Authenticate Docker to ECR
def authenticate_docker_to_ecr(repo_uri):
    subprocess.run(f"aws ecr get-login-password --region {aws_region} | docker login --username AWS --password-stdin {repo_uri}", shell=True)

# Step 3: Build and Push Docker Image to ECR
def build_and_push_docker_image(repo_uri, dockerfile_dir):
    subprocess.run(f"docker build -t {repo_uri} {dockerfile_dir}", shell=True)
    subprocess.run(f"docker push {repo_uri}", shell=True)

# Step 4: Create an EKS Cluster
def create_eks_cluster(cluster_name):
    response = eks_client.create_cluster(
        name=cluster_name,
        version="1.21",  # Specify the desired Kubernetes version
        roleArn="arn:aws:iam::your-account-id:role/your-eks-role",  # Provide the IAM role for EKS
        resourcesVpcConfig={
            "subnetIds": ["subnet-xxx", "subnet-yyy"],  # Replace with your subnet IDs
            "securityGroupIds": ["sg-xxx"]  # Replace with your security group IDs
        }
    )
    return response['cluster']

# Step 5: Deploy Kubernetes Manifest
def deploy_k8s_manifest(cluster_name, manifest_file):
    # Use a Kubernetes CLI (kubectl) to apply the manifest
    subprocess.run(f"kubectl apply -f {manifest_file} --kubeconfig kubeconfig-{cluster_name}", shell=True)

# Main Execution
if __name__ == "__main__":
    try:
        # Step 1: Create ECR Repository
        ecr_repo = create_ecr_repository(ecr_repository_name)
        ecr_repo_uri = ecr_repo['repositoryUri']

        # Step 2: Authenticate Docker to ECR
        authenticate_docker_to_ecr(ecr_repo_uri)

        # Step 3: Build and Push Docker Image to ECR
        build_and_push_docker_image(ecr_repo_uri, "path/to/your/dockerfile-directory")

        # Step 4: Create EKS Cluster
        eks_cluster = create_eks_cluster(eks_cluster_name)

        # Wait for the cluster to become active (this may take several minutes)
        while eks_cluster['status'] != "ACTIVE":
            time.sleep(10)
            eks_cluster = eks_client.describe_cluster(name=eks_cluster_name)

        # Step 5: Deploy Kubernetes Manifest
        deploy_k8s_manifest(eks_cluster_name, k8s_manifest_file)

        print("EKS cluster and Kubernetes application deployment completed successfully.")

    except Exception as e:
        print(f"Error: {e}")
