#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is the main script to run the subscripts, currently this will
run mythfilldatabase and then send a trucated log file through email
so I know it ran.
"""

# imports included with python
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from datetime import datetime, time
import subprocess

# Personal imports
from tmod import (
    config_setup_myth,
    open_file,
    open_yaml,
    check_file_age,
    get_config,
    last_n_lines,
    decrypt_login,
    mail,
    check_dir,
)
from mupdate import update_myth_DB
from mail_log import mail_body

__author__ = "Troy Franks"
__version__ = "2023-03-23"

conf_dir = ".config/mythupdate"
conf_file = "mythupdate_set.yaml"


def runtime():
    settings = open_yaml(
        fname=f"{conf_dir}/{conf_file}",
        fdest="home",
    )
    return settings["runtime"]


def call_funtion():
    config = get_config(
        conf_dir=conf_dir,
        conf_file=conf_file,
    )
    kf = f"{conf_dir}/.info.key"
    ef = f"{conf_dir}/.cred_en.yaml"
    send_to = config["sendto"]
    log = config["logs"]
    lines = config["lines"]

    update_myth_DB(settings)
    print("mythfilldatabse was run, check the log file for details")
    today_date = datetime.today().date()
    subject = f"mythfilldatabase run: {today_date}(Log file: {log})"
    body = mail_body(
        filename=log,
        lines=lines,
        fdest="relative",
    )
    key = open_file(fname=kf, fdest="home", mode="rb")
    login = decrypt_login(key=key, e_fname=ef, fdest="home")
    mail(
        body=body,
        subject=subject,
        send_to=send_to,
        login=login,
    )


# def mail_body(filename, lines):
#     age = check_file_age(filename, "relative")
#     if age >= 24:
#         con = f"The log file {filename} " f"is {age} hours old check backup"
#     else:
#         fcon = last_n_lines(fname=filename, lines=lines, fdest="relative")
#         con = f"File age: {age} hours \n{fcon}"
#     return con


dir_exist = check_dir(conf_dir)
if dir_exist is False:
    config_setup_myth(conf_dir, conf_file)
every().day.at(str(runtime())).do(call_funtion)

if __name__ == "__main__":
    try:
        print("waiting on timer")
        while True:
            run_pending()
            sleep(1)
    except KeyboardInterrupt as e:
        print(e)
        print("Interrupted")
