import yaml
import os
from ASAPP.backend.utils.logger import LoggerManager

logger = LoggerManager(use_console=True)

def load_config(path="../../config.yml"):
    try:
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
        with open(absolute_path, "r") as file:
            config = yaml.safe_load(file)

            backend_url = os.getenv("BACKEND_URL")
            if backend_url:
                config["api"]["create_project"] = f"{backend_url}/create_project"
                config["api"]["chat"] = f"{backend_url}/chat"

            logger.log("INFO", "Loading Config", {"message": "Config loaded Successfully."})
            return config

    except FileNotFoundError:
            logger.log("INFO", "Config not found.", {"message": "Config file not found."})

    except yaml.YAMLError as e:
        logger.log("ERROR", "Config Parse Error", {"error": str(e)})
        return None

    except Exception as e:
        logger.log("ERROR", "Config Load Failed", {"error": str(e)})
        return None

config = load_config()

PLAN_MODEL = config["model"]["planner"]

CREATE_PROJECT_URL= config["api"]["create_project"]
CHAT_URL = config["api"]["chat"]
