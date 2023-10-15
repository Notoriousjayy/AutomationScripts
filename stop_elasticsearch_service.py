import subprocess

def stop_elasticsearch():
    try:
        # Stop Elasticsearch
        elasticsearch_stop_command = "sudo systemctl stop elasticsearch"
        subprocess.run(elasticsearch_stop_command, shell=True, check=True)
        print("Elasticsearch service stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to stop Elasticsearch
stop_elasticsearch()
