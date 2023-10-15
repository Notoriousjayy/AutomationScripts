import subprocess

def restart_services():
    try:
        # Restart rsyslog
        rsyslog_command = "sudo systemctl restart rsyslog"
        subprocess.run(rsyslog_command, shell=True, check=True)
        print("rsyslog service restarted successfully.")

        # Restart Logstash
        logstash_command = "sudo systemctl restart logstash"
        subprocess.run(logstash_command, shell=True, check=True)
        print("Logstash service restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to restart services
restart_services()
