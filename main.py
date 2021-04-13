# -*- coding: utf-8 -*-
version = '2021-04-12'
from datetime import datetime
from tmod import open_file, open_yaml, check_file_age, last_n_lines
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser
from os import environ
import subprocess

username = getuser()
timer = open_file('.mupdatetimer', 'home', '05:00')
print(timer)

def  call_funtion():
  print(username)
  with open('mupdate.log', 'w') as file:
    update = subprocess.run(['mythfilldatabase'], stdout=file, text=True)
  print('mythfilldatabse was run, check the log file for details')
  today_date = datetime.today().date()
  filename = 'mupdate.log'
  subject = f'mythfilldatabase run: {today_date}(Log file: {filename})'
  body = mail_body(filename, 100,)
  mail(body, subject)
 
def mail_body(filename, lines):
  age =  check_file_age(filename)
  print(f'file age {age} hours')
  if age >= 24:
    con = f"The log file {filename} for {username} is {age} hours old check backup"
  else:
    con = last_n_lines(filename, lines, 'relative')
  return con

def login_info():
  ps = open_yaml('.cred.yaml', 'home')
  for key, value in ps.items():
    us = key
    psw = value
  return [us,psw]

def mail(body, subject):
  us, psw = login_info()
  recipients = open_file('.send', 'home').splitlines()
  message = f'Subject: {subject}\n\n{body}'
  print(message)
  try:
    mail = SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(us, psw)
    mail.sendmail(us,recipients, message)
    mail.close()
    print('Successfully sent email')
  except Exception as e:
    print('Could not send email because')
    print(e)


every().day.at(timer).do(call_funtion)

if __name__ == "__main__":
  try:
    print('waiting on timer')
    while True:
      run_pending()
      sleep(1)
  except KeyboardInterrupt as e:
    print(e)
    print('Interrupted')