#!/usr/bin/python
#Prior to running this, make sure cx_Oracle is installed on this machine
import sys
import cx_Oracle
import os
import getpass
import smtplib

sender_email = raw_input("Sender Email: ")
reciever_email = raw_input("Receiver Email: ")
error_log = 'error_log'

def send_email(email_send):
    s = smtplib.SMTP('localhost')
    if email_send:
        message_text = open(write_file).read()
        message_subject = "Job passed"
        message = 'Subject: %s\n\n%s' %(message_subject, message_text)
        s.sendmail(sender_email, receiver_email, message)
    else:
        error_message_text = open(error_log).read()
        error_message_subject = "Job Errored"
        error_message = 'Subject: %s\n\n%s' %(error_message_subject, error_message_text)
        s.sendmail(sender_email, receiver_email, error_message)

def printf (format,*args):
    error_target = open(error_log, "w")
    error_target.write(format % args)
    error_target.close()  

def printException (exception):
    error, = exception.args
    printf ("Error code = %s\n",error.code);
    printf ("Error message = %s\n",error.message);

username = raw_input("Enter username: ")
password = getpass.getpass("Enter password: ")
databaseName = raw_input("Enter database conn string: ")

try:
  connection = cx_Oracle.connect (username,password,databaseName)
except cx_Oracle.DatabaseError, exception:
  printf ('Failed to connect to %s\n',databaseName)
  printException (exception)
  send_email(False)
  exit (1)

cursor = connection.cursor ()

try:
  cursor.execute ('')
except cx_Oracle.DatabaseError, exception:
  printf ('Failed to run query\n')
  printException (exception)
  send_email(False)
  exit (1)

write_file = 'test_logs'

try:
    target = open(write_file,"w")
except IOError:
    target = open(write_file,"w")

for row in cursor.fetchall():
    target.write("COLUMN1:%s" % row[1])
    target.write("\n")
    target.write("COLUMN2:%s" %row[2])
    target.write("\n")
    target.write("COLUMN3:%s" %row[3])
    target.write("\n")

cursor.close ()
connection.close ()
target.close()

if os.stat("test_logs").st_size > 0:
    send_email(True)

exit(0)
