import pytest
import os
import yaml
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from process_yaml import modify_topic_yaml_with_config

@pytest.fixture
def initial_yaml_file(tmp_path):
    # Create a sample initial YAML file for testing
    initial_yaml = {
        'apiVersion': 'platform.confluent.io/v1beta1',
        'kind': 'KafkaTopic',
        'metadata': {
            'name': 'sample-topic',
            'namespace': 'default'
        },
        'spec': {
            'partitions': 3,
            'replicas': 1
        }
    }
    initial_yaml_path = tmp_path / "initial.yaml"
    with open(initial_yaml_path, 'w') as file:
        yaml.dump(initial_yaml, file)
    return initial_yaml_path

@pytest.fixture
def config_file(tmp_path):
    # Create a sample config YAML file for testing
    config_yaml = {
        'namespace': 'test-namespace',
        'prefix': 'test-prefix-'
    }
    config_yaml_path = tmp_path / "config.yaml"
    with open(config_yaml_path, 'w') as file:
        yaml.dump(config_yaml, file)
    return config_yaml_path

def test_modify_topic_yaml_with_config(initial_yaml_file, config_file, tmp_path):
    output_directory = tmp_path
    modify_topic_yaml_with_config(str(initial_yaml_file), str(output_directory), str(config_file))

    expected_filename = output_directory / "test-prefix-sample-topic.yaml"
    assert os.path.exists(expected_filename)

    with open(expected_filename, 'r') as modified_file:
        modified_yaml = yaml.safe_load(modified_file)

    assert modified_yaml['metadata']['namespace'] == 'test-namespace'
    assert modified_yaml['metadata']['name'] == 'test-prefix-sample-topic'

def test_modify_topic_yaml_with_default_config(initial_yaml_file, tmp_path):
    output_directory = tmp_path
    modify_topic_yaml_with_config(str(initial_yaml_file), str(output_directory), "non_existing_config.yaml")

    expected_filename = output_directory / "sample-topic.yaml"
    assert os.path.exists(expected_filename)

    with open(expected_filename, 'r') as modified_file:
        modified_yaml = yaml.safe_load(modified_file)

    assert modified_yaml['metadata']['namespace'] == 'default'
    assert modified_yaml['metadata']['name'] == 'sample-topic'
