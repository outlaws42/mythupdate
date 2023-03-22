#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script sends notifications with a section of backup log files through the
ntfy service. This will run at a specified time from the config.
"""
# Imports
from schedule import run_pending, every
from time import sleep
from getpass import getuser
import requests

# Personal Imports
from tmod import open_yaml, check_dir, config_setup_myth, open_file
from create_log import create_file, get_config
from mupdate import update_myth_DB

__author__ = "Troy Franks"
__version__ = "2023-03-22"

# Global Variables
username = getuser()
conf_dir: str = ".config/mythupdate"
conf_file: str = "mythupdate_set.yaml"


def runtime():
    settings = open_yaml(
        fname=f"{conf_dir}/{conf_file}",
        fdest="home",
    )
    return settings["runtime"]


def send_file():
    config = get_config(
        conf_dir,
        conf_file,
    )
    update_myth_DB(config)
    create_file(
        config_setting=config,
        location="relative",
    )
    logs = config["logs"]
    lines = config["lines"]
    topic = config["topic"]

    requests.put(
        f"https://ntfy.sh/{topic}",
        data=open_file(
            fname=f"{logs}.txt",
            fdest="relative",
            mode="rb",
        ),
        headers={"Filename": f"{logs}.txt"},
    )


dir_exist = check_dir(conf_dir)
if dir_exist is False:
    config_setup_myth(conf_dir)
every().day.at(str(runtime())).do(send_file)

if __name__ == "__main__":
    try:
        print("waiting on timer")
        while True:
            run_pending()
            sleep(1)
    except KeyboardInterrupt as e:
        print(e)
        print("Interrupted")
