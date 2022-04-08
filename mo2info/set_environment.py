import json
import os


def set_environment():
    if (
            os.environ.get("DJANGO_SETTINGS_MODULE")
            == "mo2info.settings.development"
    ):
        return
    with open("/mo2info/env.json", "r") as envfile:
        eb_env = json.load(envfile)
        for k,v in eb_env.items():
            os.environ.setdefault(k, v)
