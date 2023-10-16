import os
import subprocess

def create_dockerfile(jar_file, java_version):
    dockerfile_content = f"""
    # Use an official Java runtime as a parent image
    FROM openjdk:{java_version}-jre-slim

    # Set the working directory inside the container
    WORKDIR /app

    # Copy the application JAR file into the container
    COPY {jar_file} .

    # Specify the command to run your Java application
    CMD ["java", "-jar", "{jar_file}"]
    """
    with open('Dockerfile', 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

def build_docker_image(image_name, image_version):
    os.system(f'docker build -t {image_name}:{image_version} .')

def push_docker_image(image_name, image_version):
    os.system(f'docker push {image_name}:{image_version}')

def main():
    # Replace these values with your project-specific details
    jar_file = 'your-app.jar'
    java_version = '11'
    image_name = 'your-java-app'
    image_version = '1.0'

    # Create Dockerfile
    create_dockerfile(jar_file, java_version)

    # Build Docker image
    build_docker_image(image_name, image_version)

    # Optionally, push the Docker image to a Docker registry (e.g., Docker Hub)
    # push_docker_image(image_name, image_version)

if __name__ == "__main__":
    main()
