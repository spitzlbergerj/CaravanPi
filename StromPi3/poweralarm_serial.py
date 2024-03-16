#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import serial
import os
import smtplib
from email.mime.text import MIMEText
##############################################################################
# This is The config for the EMAIL notification
##############################################################################
SERVER =    'SMTP.Server.Com'
PORT =      587
EMAIL =    'Example@Example.com'
PASSWORT =  'Password'
EMPFAENGER =    ['EmpfÃ¤nger@Example.com' ,]
SUBJECT_Powerfail =   'Raspberry Pi Powerfail!'  #Powerfail Email Betreff
SUBJECT_Powerback =   'Raspberry Pi Powerback!'  #Powerback Email Betreff
SUBJECT_Restart =     'Raspberry Pi Restart!'    #Restart Email Betreff
##############################################################################
# Here you can choose whether you want to receive an email when the Raspberry Pi restarts - 1 to activate - 0 to deactivate
Restart_Mail = 0
##############################################################################
t=0 #Temporary time-variable
##############################################################################

def Detect_Powerfail():
    while 1:
     x=ser.readline()
     y = x.decode(encoding='UTF-8',errors='strict')
     if y==('xxxShutdownRaspberryPixxx\n') or y==('xxx--StromPiPowerfail--xxx\n'):
      print ("PowerFail - Email Sent")
      Sendmail_Powerfail()

def Sendmail_Powerback():
    BODY =      """
    <html>
     <head></head>
      <body>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg .tg-0ord{text-align:right}
    .tg .tg-qnmb{font-weight:bold;font-size:16px;text-align:center}
    </style>
    <table class="tg">
     <tr>
      <th class="tg-qnmb" colspan="2">StromPi hat Spannung wiedererkannt!</th>
     </tr>
    </table>
     </body>
    </html>
    """

    session = smtplib.SMTP(SERVER, PORT)
    session.set_debuglevel(1)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(EMAIL, PASSWORT)
    msg = MIMEText(BODY, 'html')
    msg['Subject'] = SUBJECT_Powerback
    msg['From'] = EMAIL
    msg['To'] = ", ".join(EMPFAENGER)
    session.sendmail(EMAIL, EMPFAENGER, msg.as_string())
    Detect_Powerfail()

def Sendmail_Restart():
    BODY =      """
    <html>
     <head></head>
      <body>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg .tg-0ord{text-align:right}
    .tg .tg-qnmb{font-weight:bold;font-size:16px;text-align:center}
    </style>
    <table class="tg">
     <tr>
      <th class="tg-qnmb" colspan="2">Ihr Raspberry Pi wurde neugestartet.</th>
     </tr>
    </table>
     </body>
    </html>
    """

    session = smtplib.SMTP(SERVER, PORT)
    session.set_debuglevel(1)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(EMAIL, PASSWORT)
    msg = MIMEText(BODY, 'html')
    msg['Subject'] = SUBJECT_Restart
    msg['From'] = EMAIL
    msg['To'] = ", ".join(EMPFAENGER)
    session.sendmail(EMAIL, EMPFAENGER, msg.as_string())
    Detect_Powerfail()
 
def Sendmail_Powerfail():
    BODY =      """
    <html>
     <head></head>
      <body>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg .tg-0ord{text-align:right}
    .tg .tg-qnmb{font-weight:bold;font-size:16px;text-align:center}
    </style>
    <table class="tg">
     <tr>
      <th class="tg-qnmb" colspan="2">StromPi hat einen STROMAUSFALL erkannt!!!!</th>
     </tr>
    </table>
     </body>
    </html>
    """

    session = smtplib.SMTP(SERVER, PORT)
    session.set_debuglevel(1)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(EMAIL, PASSWORT)
    msg = MIMEText(BODY, 'html')
    msg['Subject'] = SUBJECT_Powerfail
    msg['From'] = EMAIL
    msg['To'] = ", ".join(EMPFAENGER)
    session.sendmail(EMAIL, EMPFAENGER, msg.as_string())
    Detect_Powerback()

def Detect_Powerback():
    while 1:
     x=ser.readline()
     y=x.decode(encoding='UTF-8',errors='strict')
     if y==('xxx--StromPiPowerBack--xxx\n'):
      print ("PowerBack - Email Sent")
      Sendmail_Powerback()

ser = serial.Serial(
 port='/dev/serial0',
 baudrate = 38400,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0

time.sleep(5) 
if Restart_Mail == 1:
  Sendmail_Restart()




	  
	  
	  
Detect_Powerfail()
