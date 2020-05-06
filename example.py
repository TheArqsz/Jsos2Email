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
from os import getenv

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
	
def main():
    jsos_username = getenv('JSOS_USERNAME')
    jsos_password = getenv('JSOS_PASSWORD')
    email_username = getenv('EMAIL_USERNAME')
    email_password = getenv('EMAIL_PASSWORD')
    if not jsos_username or not jsos_password or not email_password or not email_username:
        log.warning("No credentials")
        exit(1)
    else:
        if not check_mail_creds(email_username, email_password):
            log.warning("Wrong credentials")
            exit(1)
        if not check_jsos_creds(jsos_username, jsos_password):
            log.warning("Wrong credentials")
            exit(1)

    with Jsos(username=jsos_username, password=jsos_password) as jsos, \
            StudentMail(email=email_username, password=email_password) as mail:
            msgs = jsos.get_messages(max=3, only_unread=True)
            for msg in msgs:
                mail.prepare_message()
                mail.prepare_headers(subject=msg['topic'])
                mail.prepare_content(content=msg['html_content'], msg_from=msg['from'])
                mail.send()

if __name__ == "__main__":
    main()