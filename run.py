#!/usr/bin/env python3

"""Example usage of Json and StudentMail classes"""

__author__ = "Arqsz"

import config
import logging

from getpass import getpass
from jsos import Jsos
from mail import StudentMail
from time import sleep as wait

log = logging.getLogger('jsos2mail')

WAIT_TIME = 240 # 4 minutes

def get_jsos_creds():
	"""Get user's credentials for JSOS"""

	ok = False
	counter = 10
	while not ok and counter>0:
		jsos_username = input("Jsos username: ")
		jsos_password = getpass("Jsos password (hidden): ")
		j = Jsos(jsos_username, jsos_password)
		ok = j.is_user_exists()
		if ok:
			return jsos_username, jsos_password
		else:
			log.warning("Try again\n")

def get_mail_creds():
	"""Get user's credentials for email"""

	ok = False
	counter = 10
	while not ok and counter>0:
		email = input("Email: ")
		email_password = getpass("Email password (hidden): ")
		s = StudentMail(email=email, password=email_password)
		ok = s.is_user_exists()
		if ok:	
			return email, email_password
		else:
			log.warning("Try again\n")



def main():
	mail, mail_password = get_mail_creds()
	jsos_username, jsos_password = get_jsos_creds()
	with Jsos(username=jsos_username, password=jsos_password) as jsos, \
			StudentMail(email=mail, password=mail_password) as mail:
		jsos.login()	
		while True:
			msgs = jsos.get_messages(max=3, only_unread=True)
			for msg in msgs:
				mail.prepare_message()
				mail.prepare_headers(subject=msg['topic'])
				mail.prepare_content(content=msg['html_content'], msg_from=msg['from'])
				mail.send()

			log.info(f"Sleeping for {WAIT_TIME} sec")
			wait(WAIT_TIME)

if __name__ == "__main__":
	main()