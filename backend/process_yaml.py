import yaml
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def modify_topic_yaml_with_config(initial_yaml_filename, output_directory, config_path):
    logging.info("Starting modification of topic YAML with configuration.")
    
    if not os.path.exists(initial_yaml_filename):
        logging.error(f"Initial YAML file '{initial_yaml_filename}' does not exist.")
        return

    logging.debug(f"Loading initial YAML from: {initial_yaml_filename}")
    with open(initial_yaml_filename, 'r') as yaml_file:
        topic_manifest = yaml.safe_load(yaml_file)
    logging.info("Successfully loaded initial YAML.")

    config = {}
    if os.path.exists(config_path):
        logging.debug(f"Loading configuration from: {config_path}")
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info("Configuration loaded successfully.")
    else:
        logging.warning(f"Configuration file '{config_path}' not found. Using default values.")

    namespace = config.get('namespace', 'default')
    prefix = config.get('prefix', '')

    logging.debug(f"Using namespace: '{namespace}' and prefix: '{prefix}'.")

    return modify_topic_yaml(topic_manifest, output_directory, namespace, prefix)

def modify_topic_yaml(topic_manifest, output_directory, namespace, prefix):
    """
    Modify the generated Kafka topic YAML file to apply the configured namespace and prefix.
    
    Args:
        topic_manifest (dict): YAML content loaded as a dictionary.
        output_directory (str): Directory where the modified YAML file will be saved.
        namespace (str): Namespace to apply to the YAML file.
        prefix (str): Prefix to prepend to the topic name in the YAML file.

    Returns:
        str: The path to the modified YAML file.
    """
    logging.info("Starting YAML modification process.")

    original_name = topic_manifest['metadata']['name']
    topic_manifest['metadata']['namespace'] = namespace
    topic_manifest['metadata']['name'] = f"{prefix}{original_name}"

    logging.debug(f"Modified topic name from '{original_name}' to '{topic_manifest['metadata']['name']}'.")
    logging.debug(f"Modified namespace to '{namespace}'.")

    if not os.path.exists(output_directory):
        logging.debug(f"Output directory '{output_directory}' does not exist. Creating it.")
        os.makedirs(output_directory)

    final_yaml_filename = f"{output_directory}/{topic_manifest['metadata']['name']}.yaml"
    logging.debug(f"Saving modified YAML to: {final_yaml_filename}")
    with open(final_yaml_filename, 'w') as yaml_file:
        yaml.dump(topic_manifest, yaml_file)

    logging.info(f"Modified YAML saved successfully to '{final_yaml_filename}'.")
    return final_yaml_filename
