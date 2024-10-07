from flask import Flask, request, jsonify
from jinja2 import Template
import yaml
from flask_cors import CORS
import os
from process_yaml import modify_topic_yaml_with_config
from github_utils import create_branch_and_pr, prepare_pr_details
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
CORS(app)

config = {}
config_path = 'topic_context_config.yaml'
if os.path.exists(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

namespace = config.get('namespace', 'default')
prefix = config.get('prefix', '')
github_token = config.get('github_token', '')
repository_name = config.get('repository_name', '')

with open('templates/kafka_topic_template.yaml', 'r') as file:
    kafka_topic_template = file.read()

@app.route('/api/create-topic', methods=['POST'])
def create_topic():
    logging.info("Received request to create Kafka topic.")

    try:
        data = request.json
        topic_name = data.get('topicName', 'default-topic')
        partitions = data.get('partitions', 3)
        replicas = data.get('replicas', 1)
        retention_days = data.get('retentionDays', 7)

        logging.debug(f"Received data - topic_name: {topic_name}, partitions: {partitions}, "
                      f"replicas: {replicas}, retention_days: {retention_days}")

        retention_ms = retention_days * 24 * 60 * 60 * 1000
        logging.debug(f"Calculated retention in milliseconds: {retention_ms}")

        template = Template(kafka_topic_template)
        rendered_yaml = template.render(
            topic_name=topic_name,
            partitions=partitions,
            replicas=replicas,
            retention_ms=retention_ms
        )
        logging.info("Successfully rendered Kafka topic YAML.")

        output_directory = 'generated_topics'
        os.makedirs(output_directory, exist_ok=True)
        initial_yaml_filename = f"{output_directory}/{topic_name}.yaml"

        logging.debug(f"Saving initial YAML to: {initial_yaml_filename}")
        with open(initial_yaml_filename, 'w') as yaml_file:
            yaml_file.write(rendered_yaml)

        logging.info("Modifying the initial YAML with configuration values.")
        final_yaml_filename = modify_topic_yaml_with_config(initial_yaml_filename, output_directory, config_path)

        logging.debug(f"Reading modified YAML from: {final_yaml_filename}")
        with open(final_yaml_filename, 'r') as yaml_file:
            modified_yaml_content = yaml_file.read()

        logging.info("Preparing branch and pull request details.")
        pr_details = prepare_pr_details(prefix, topic_name)

        try:
            logging.info("Creating a branch and pull request on GitHub.")
            pr_url = create_branch_and_pr(
                github_token=github_token,
                repository_name=repository_name,
                branch_name=pr_details["branch_name"],
                filename=pr_details["filename"],
                content=modified_yaml_content,
                pr_title=pr_details["pr_title"],
                pr_body=pr_details["pr_body"]
            )
            logging.info(f"Pull request successfully created: {pr_url}")
        except Exception as e:
            logging.error(f"Failed to create pull request: {str(e)}")
            return jsonify({"error": f"Failed to create pull request: {str(e)}"}), 500

        return jsonify({
            "message": f"Kafka topic YAML file '{final_yaml_filename}' created successfully",
            "pull_request_url": pr_url
        }), 201

    except Exception as e:
        logging.error(f"An error occurred during topic creation: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
