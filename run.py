#!/usr/bin/env python3

"""Example usage of Json and StudentMail classes"""

__author__ = "Arqsz"

import config
import logging
import argparse

from getpass import getpass
from jsos import Jsos
from mail import StudentMail
from time import sleep as wait

log = logging.getLogger('jsos2mail')

def get_jsos_creds():
	"""Get user's credentials for JSOS"""

	ok = False
	counter = 10
	while not ok and counter>0:
		jsos_username = input("Jsos username: ")
		jsos_password = getpass("Jsos password (hidden): ")
		ok = check_jsos_creds(jsos_username, jsos_password)
		if ok:
			return jsos_username, jsos_password
		else:
			log.warning("Try again\n")
	log.warning("Wrong credentials")
	exit(1)

def get_mail_creds():
	"""Get user's credentials for email"""

	ok = False
	counter = 10
	while not ok and counter>0:
		email = input("Email: ")
		email_password = getpass("Email password (hidden): ")
		ok = check_mail_creds(email, email_password)
		if ok:	
			return email, email_password
		else:
			log.warning("Try again\n")
	log.warning("Wrong credentials")
	exit(1)

def check_mail_creds(email, password):
	"""Checks if credentials are correct"""

	s = StudentMail(email=email, password=password)
	return s.is_user_exists()


def check_jsos_creds(username, password):
	"""Checks if credentials are correct"""

	j = Jsos(username, password)
	return j.is_user_exists()
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("--wait-time", "-w", help="duration of wait time between scans",
                    type=int, default=240)
	parser.add_argument("--input", "-i", help="sets script to let you type your credentials in (default)", default=True,
                    type=bool)
	parser.add_argument("--no-input", "-n", help="you have to provide your credentials with CLI arguments", default=False,
                    type=bool)
	parser.add_argument("--jsos-usr", help="jsos username", type=str)
	parser.add_argument("--jsos-pwd", help="jsos password", type=str)
	parser.add_argument("--email", help="your email", type=str)
	parser.add_argument("--email-pwd", help="your email's password", type=str)				

	args = parser.parse_args()

	WAIT_TIME = args.wait_time

	if not args.no_input:
		mail, mail_password = get_mail_creds()
		jsos_username, jsos_password = get_jsos_creds()
	else:
		if args.email and args.email_pwd and args.jsos_usr and jsos_pwd:
			mail = args.email
			mail_password = args.email_pwd
			if not check_mail_creds(mail, mail_password):
				log.warning("Wrong credentials")
				exit(1)
			jsos_username = args.jsos_urs
			jsos_password = args.jsos_pwd
			if not check_jsos_creds(jsos_username, jsos_password):
				log.warning("Wrong credentials")
				exit(1)
		else:
			log.warning("No data provided")
			exit(1)

	with Jsos(username=jsos_username, password=jsos_password) as jsos, \
			StudentMail(email=mail, password=mail_password) as mail:
		while True:
			msgs = jsos.get_messages(max=3, only_unread=True)
			for msg in msgs:
				mail.prepare_message()
				mail.prepare_headers(subject=msg['topic'])
				mail.prepare_content(content=msg['html_content'], msg_from=msg['from'])
				mail.send()

			log.info(f"Sleeping for {WAIT_TIME} sec")
			try:
				wait(WAIT_TIME)
			except KeyboardInterrupt:
				exit(1)