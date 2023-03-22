#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This creates a copy of a log file with only the last so many lines for sending
for sending with notifications.
"""

# Imports
from getpass import getuser
from datetime import datetime, time
import subprocess

# Personal Imports
from tmod import open_yaml

__author__ = "Troy Franks"
__version__ = "2023-03-21"

# Global Variables
username = getuser()
conf_dir: str = ".config/mythupdate"
conf_file: str = "mythupdate_set.yaml"


def get_config():
    settings = open_yaml(
        fname=f"{conf_dir}/{conf_file}",
        fdest="home",
    )
    return settings


def update_myth_DB(config_setting):
    config = config_setting
    log = config["logs"]
    lines = config["lines"]

    with open(log, "w") as file:
        update = subprocess.run(["mythfilldatabase"], stdout=file, text=True)


if __name__ == "__main__":
    config = get_config()
    update_myth_DB(config)
