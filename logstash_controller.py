import subprocess
import os
import time

# Define the Logstash executable path
logstash_executable = "/path/to/logstash/bin/logstash"  # Replace with the actual path to your Logstash executable

# Define the Logstash configuration file path
logstash_config = "/path/to/your/logstash.conf"  # Replace with the actual path to your Logstash configuration file

# Function to check if Logstash is already running
def is_logstash_running():
    try:
        # Use subprocess to check if Logstash process is running
        subprocess.check_output(["pgrep", "-f", logstash_executable])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to start Logstash
def start_logstash():
    if is_logstash_running():
        print("Logstash is already running.")
    else:
        print("Starting Logstash...")
        subprocess.Popen([logstash_executable, "-f", logstash_config], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Logstash has been started.")

# Function to stop Logstash
def stop_logstash():
    if is_logstash_running():
        print("Stopping Logstash...")
        subprocess.call(["pkill", "-f", logstash_executable])
        print("Logstash has been stopped.")
    else:
        print("Logstash is not running.")

# Main function
if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Start Logstash")
        print("2. Stop Logstash")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            start_logstash()
        elif choice == "2":
            stop_logstash()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    print("Exiting the script.")
