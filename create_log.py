#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This creates a copy of a log file with only the last so many lines for sending
for sending with notifications.
"""

# Imports
from getpass import getuser

# Personal Imports
from tmod import (
    save_file,
    open_yaml,
    check_file_age,
    last_n_lines,
)

__author__ = "Troy Franks"
__version__ = "2023-03-22"

# Global Variables
username = getuser()


def get_config(
    conf_dir: str,
    conf_file: str,
):
    settings = open_yaml(
        fname=f"{conf_dir}/{conf_file}",
        fdest="home",
    )
    return settings


def create_file(
    config_setting,
    location: str,
):
    config = config_setting
    logs = config["logs"]
    lines = config["lines"]

    body = file_body(
        filename=logs,
        lines=lines,
        fdest=location,
    )
    save_file(
        fname=f"{logs}.txt",
        content=body,
        fdest=location,
        mode="w",
    )


def file_body(
    filename: str,
    lines: int,
    fdest: str = "home",
):
    age: int = check_file_age(filename, fdest)
    if age >= 24:
        body: str = (
            f"The log file {filename} for "
            f"{username} is {age} hours old check backup"
        )
    else:
        truncated_file = last_n_lines(
            fname=filename,
            lines=lines,
            fdest=fdest,
        )
        body = f"File age: {age} hours for user {username}\n{truncated_file}"
    return body


if __name__ == "__main__":
    config = get_config()
    config_dir = ".config"
    conf_file = "emailog_set.yaml"
    create_file(config)
