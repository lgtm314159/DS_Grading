#!/usr/bin/env python

from os import *
from sys import *
from glob import *
from re import *
from smtplib import SMTP_SSL as SMTP
from email.MIMEText import MIMEText

for f in sorted(listdir('.')):
  # f is a student's NetId, e.g. jx372
  if not match('.*[0-9]$', f): continue
  lines = file('results/%s.out' % f).read().split('\n')
  success = 'ONE OR MORE TESTS FAILED'
  stdout = file('results/%s.out' % f).read()
  stderr = file('results/%s.err' % f).read()
  for l in lines:
    if 'passed all tests' in l:
      success = 'ALL TESTS PASSED'
  body = '''
Student ID: %(f)s
Results for lab 1: %(success)s
If you have questions about these results, contact junyang.xin@nyu.edu.

Standard out:

%(stdout)s

Standard err:

%(stderr)s

''' % locals()
  conn = SMTP('SMTP.nyu.edu')
  conn.set_debuglevel(False)
  email = 'your_nyu_email'
  passwd = 'your_email_password'
  conn.login(email, passwd)
  msg = MIMEText(body)
  msg['Subject'] = 'Testing results for lab 1'
  msg['From'] = email
  msg['Bcc'] = 'professor_email_if_necessary' 
  msg['To'] = f + '@nyu.edu'
  conn.sendmail(email, f + '@nyu.edu', msg.as_string()) 
  print 'Sent', f 
