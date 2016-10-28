import time
import os
import subprocess
import shutil
import sys
import atexit

read_file = raw_input("Enter the name of the file to read: ")
write_file = raw_input("Enter the name of the file to write into: ")
email_sent = False
LOG_LEVEL = raw_input("Enter Log Level(FATAL|ERROR|WARN|INFO): ")
email_address = raw_input("Enter email address: ")

#Write to an external file
def write_to_file():

    file_to_read = open(read_file,"r")
    try:
	file_to_write = open(write_file,"r+b")
    except IOError:
	print ('File not found. So creating new one')
	file_to_write = open(write_file,"w")

    start_time = time.time()
    end_time=0
    global email_sent
    email_sent = False

    while 1:
	if email_sent is True:
	    start_time = time.time()
	    email_sent = False
	    print "Begin Monitoring Again..."
	    file_to_write = open(write_file,"r+b")

        where = file_to_read.tell()
        line = file_to_read.readline()
        if not line:
            time.sleep(1)
	    end_time = time.time()
 	    file_to_read.seek(where)
   	    if end_time - start_time > 10:
                send_email(file_to_write)
        else:
	    diff = end_time-start_time
	    if diff<10:
		end_time = time.time()
		if LOG_LEVEL in line:
	            file_to_write.write(line)
		    continue
	    else:
		send_email(file_to_write)

def send_email(file_to_write):
    email_sent=True
    file_to_write.close()
    global email_address

    # Close the file, email it to user, rm the file, create new one in that dir
    if os.stat(write_file).st_size != 0:
        print "Content found. Emailing user"

        os.system('mail -v -s "Monitor Logs Test" %s < %s' % (email_address, write_file))
        print 'Removing existing file'
        os.system('rm %s' % write_file)
        print 'Creating new file'
        os.system('touch %s' %write_file)

def exit_handler():
    print "Exiting.... Removing %s" %write_file
    os.system('rm %s' % write_file)

def main():
    try:
        write_to_file()
    finally:
        atexit.register(exit_handler)

if __name__=='__main__':
    main()
