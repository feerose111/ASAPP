import yaml
import os

def load_config(path="../../config.yml"):
    absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
    with open(absolute_path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

PLAN_MODEL = config["model"]["planner"]

CREATE_PROJECT_API = config["api"]["create_project"]
