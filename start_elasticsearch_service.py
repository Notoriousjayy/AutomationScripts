import subprocess

def start_elasticsearch():
    try:
        # Start Elasticsearch
        elasticsearch_start_command = "sudo systemctl start elasticsearch"
        subprocess.run(elasticsearch_start_command, shell=True, check=True)
        print("Elasticsearch service started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to start Elasticsearch
start_elasticsearch()
