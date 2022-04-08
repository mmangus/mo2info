import json
import os


def set_environment():
    with open("env.json", "r") as envfile:
        eb_env = json.load(envfile)
        for k,v in eb_env.items():
            os.environ.setdefault(k, v)
