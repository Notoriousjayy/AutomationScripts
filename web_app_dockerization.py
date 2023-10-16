import os

def create_dockerfile(directory, image_name, node_version, entry_point):
    dockerfile_content = f"""
    FROM node:{node_version}
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    COPY . .
    EXPOSE 80
    CMD ["node", "{entry_point}"]
    """
    with open(os.path.join(directory, 'Dockerfile'), 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

def build_docker_image(directory, image_name, image_version):
    os.chdir(directory)
    os.system(f'docker build -t {image_name}:{image_version} .')

def generate_docker_compose(directory, backend_image, frontend_image):
    docker_compose_content = f"""
    version: '3'
    services:
      backend:
        image: {backend_image}
        ports:
          - "8080:8080"
        restart: always

      frontend:
        image: {frontend_image}
        ports:
          - "80:80"
        restart: always
    """
    with open(os.path.join(directory, 'docker-compose.yml'), 'w') as docker_compose_file:
        docker_compose_file.write(docker_compose_content)

def main():
    # Replace these values with your project-specific details
    backend_directory = 'backend'
    frontend_directory = 'frontend'
    backend_image_name = 'your-backend-name'
    frontend_image_name = 'your-frontend-name'
    node_version = '14'
    backend_entry_point = 'server.js'
    frontend_entry_point = 'serve -s build'
    backend_image_version = '1.0'
    frontend_image_version = '1.0'

    # Create Dockerfiles
    create_dockerfile(backend_directory, backend_image_name, node_version, backend_entry_point)
    create_dockerfile(frontend_directory, frontend_image_name, node_version, frontend_entry_point)

    # Build Docker images
    build_docker_image(backend_directory, backend_image_name, backend_image_version)
    build_docker_image(frontend_directory, frontend_image_name, frontend_image_version)

    # Generate Docker Compose file (optional)
    generate_docker_compose('.', backend_image_name, frontend_image_name)

if __name__ == "__main__":
    main()
