import os

# Function to generate a Logstash configuration file
def generate_logstash_config(log_file_path, graphite_host, graphite_port, metric_path):
    config = f"""
input {{
  file {{
    path => "{log_file_path}"
    start_position => "beginning"
  }}
}}

filter {{
  # Add filters here if needed to parse and structure log data
}}

output {{
  graphite {{
    host => "{graphite_host}"
    port => {graphite_port}
    metrics => ["{metric_path}"]
  }}
}}
"""
    return config

# Main function
if __name__ == "__main__":
    # Customize these variables with your specific configuration
    log_file_path = "/var/log/syslog"
    graphite_host = "graphite-server.example.com"
    graphite_port = 2003
    metric_path = "your.metric.path"

    # Generate the Logstash configuration
    logstash_config = generate_logstash_config(log_file_path, graphite_host, graphite_port, metric_path)

    # Save the configuration to a file
    config_file_path = "logstash.conf"
    with open(config_file_path, "w") as config_file:
        config_file.write(logstash_config)

    print(f"Logstash configuration has been saved to {config_file_path}")
