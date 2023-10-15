import os
import subprocess

# Define your application details
application_name = "your-application"
docker_image_name = "your-docker-image"
docker_image_tag = "latest"

# Define Dockerfile content
dockerfile_content = f"""\
# Stage 1: Build the application
FROM maven:3.8.3-openjdk-11 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src src
RUN mvn package -DskipTests

# Stage 2: Create the application image
FROM adoptopenjdk:11-jre-hotspot
COPY --from=build /app/target/{application_name}.jar /app.jar
CMD ["java", "-jar", "/app.jar"]
"""

# Create a Dockerfile
with open("Dockerfile", "w") as dockerfile:
    dockerfile.write(dockerfile_content)

# Build the Docker image
subprocess.run(["docker", "build", "-t", f"{docker_image_name}:{docker_image_tag}", "."])

# Remove the temporary Dockerfile
os.remove("Dockerfile")

# Run a container using the newly created image
subprocess.run(["docker", "run", "-d", "-p", "host-port:container-port", f"{docker_image_name}:{docker_image_tag}"])

print(f"Successfully built and started the {docker_image_name}:{docker_image_tag} container.")
