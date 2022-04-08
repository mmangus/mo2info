#!/bin/env python3
import json
import subprocess

if __name__ == "__main__":
    eb_environment = json.loads(
        subprocess.run(
            [
                "/opt/elasticbeanstalk/bin/get-config",
                "environment"
            ],
            capture_output=True
        ).stdout
    )
    with open("/var/app/staging/env.json", "w") as outfile:
        json.dump(eb_environment, outfile)
