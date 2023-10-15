import os

# Define the Logstash server hostname or IP address and port
logstash_server = "logstash-server"
logstash_port = "514"

# Define the Rsyslog configuration snippet for forwarding logs
forwarding_config = f"*.* @{logstash_server}:{logstash_port}"

# Define the path to the Rsyslog configuration file
rsyslog_config_file = "/etc/rsyslog.conf"

def configure_rsyslog_forwarding():
    try:
        # Open the Rsyslog configuration file for appending
        with open(rsyslog_config_file, "a") as f:
            # Append the forwarding configuration to the end of the file
            f.write("\n# Forward logs to Logstash\n")
            f.write(forwarding_config + "\n")

        # Restart the Rsyslog service to apply the new configuration
        os.system("sudo service rsyslog restart")

        print("Rsyslog configuration updated. Logs will be forwarded to Logstash.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    configure_rsyslog_forwarding()
