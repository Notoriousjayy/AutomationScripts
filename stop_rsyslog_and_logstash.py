import subprocess

def stop_services():
    try:
        # Stop rsyslog
        rsyslog_command = "sudo systemctl stop rsyslog"
        subprocess.run(rsyslog_command, shell=True, check=True)
        print("rsyslog service stopped successfully.")

        # Stop Logstash
        logstash_command = "sudo systemctl stop logstash"
        subprocess.run(logstash_command, shell=True, check=True)
        print("Logstash service stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to stop services
stop_services()
