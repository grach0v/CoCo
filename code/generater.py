import argparse
import yaml
import sys

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error reading YAML file: {exc}")
            sys.exit(1)

def main(yaml_file):
    params = load_yaml(yaml_file)
    print("Parameters loaded from YAML file:")

    for key, value in params.items():
        print(f"{key}: {value}")



# if __name__ == "__main__":
    
#     if len(sys.argv) != 2:
#         print("Usage: python generater.py <path_to_yaml_file>")
#         sys.exit(1)

#     parser = argparse.ArgumentParser(description='Generate dataset and test a model using yaml config.')
#     parser.add_argument('yaml_file', type=str, help='Path to the YAML file')
#     args = parser.parse_args()

#     main(args.yaml_file)
