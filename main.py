## -*- coding: utf-8 -*-
version = '2021-05-01'

from tmod import (
  config_setup_myth, open_file, 
  open_yaml, check_file_age, last_n_lines,
  decrypt_login, mail, check_dir
  )
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from datetime import datetime, time
import subprocess

conf_dir = ".config/mythupdate"
conf_file = 'mythupdate_set.yaml'

def runtime():
  settings = open_yaml(
  fname = f"{conf_dir}/{conf_file}",
  fdest = "home",
  )
  return settings['runtime']

def  call_funtion():
  settings = open_yaml(
  fname = f"{conf_dir}/{conf_file}",
  fdest = "home",
  )
  kf = f"{conf_dir}/.info.key"
  ef = f"{conf_dir}/.cred_en.yaml"
  st = settings['sendto']
  log = settings['logs']
  lines = settings['lines']

  with open(log, 'w') as file:
    update = subprocess.run(['mythfilldatabase'], stdout=file, text=True)
  print('mythfilldatabse was run, check the log file for details')
  today_date = datetime.today().date()
  sub = f'mythfilldatabase run: {today_date}(Log file: {log})'
  body = mail_body(log, lines)
  key = open_file(
      fname = kf, 
      fdest = "home",
      mode ="rb"
      )
  login = decrypt_login(
    key = key, 
    e_fname = ef, 
    fdest = "home"
      )
  mail(
    body = body, 
    subject = sub, 
    send_to = st,
    login = login
        )
 
def mail_body(filename, lines):
  age =  check_file_age(filename, 'relative')
  if age >= 24:
    con = (
      f"The log file {filename} " 
      f"is {age} hours old check backup")
  else:
    fcon = last_n_lines(
      fname = filename, 
      lines=lines,
      fdest = "relative"
      )
    con = f'File age: {age} hours \n{fcon}'
  return con

dir_exist = check_dir(conf_dir)
if dir_exist == False:
  config_setup_myth(conf_dir, conf_file)
every().day.at(str(runtime())).do(call_funtion)

if __name__ == "__main__":
  try:
    print('waiting on timer')
    while True:
      run_pending()
      sleep(1)
  except KeyboardInterrupt as e:
    print(e)
    print('Interrupted')