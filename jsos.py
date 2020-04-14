#!/usr/bin/env python3

"""Wrapper for JSOS (WUST-based website)

This class allows to connect to JSOS end extract data such as:
- messages
"""

__author__ = 'Arqsz'

from time import sleep as wait
from bs4 import BeautifulSoup
import requests as r
import config
import logging 

log = logging.getLogger('jsos2mail')

class Jsos():
	"""
	Class that allows to connect with JSOS website.

	...

	Attributes
    ----------
    username : str
        the username of the user
    password : str
        the password of the user

    Methods
    -------
    login(is_test=False)
        Logs user in to JSOS
	"""

	def __init__(self, username: str, password: str):
		"""
        Parameters
        ----------
        username : str
            the username of the user
        password : str
            the password of the user
        """

		self.session = r.Session()
		self.base_oauth_url = "https://oauth.pwr.edu.pl"
		self.base_jsos_url = "https://jsos.pwr.edu.pl"
		self.username = username
		self.password = password
		self.__is_logged = False

	def __enter__(self): 
		log.info("Starting coonnection with JSOS")
		self.login()
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback): 
		log.info("Closing coonnection with JSOS")
		self.logout(force=True)

	def login(self, is_test: bool = False):
		"""Logs user in to JSOS.

        If the argument `is_test` isn't passed in, connection is checked 10 times. 
        If the argument `is_test` is passed in, connection is checked one time.

        Parameters
        ----------
        is_test : bool, optional
            is this method used to test connection (default is False)

        Raises
        ------
        JsosConnectionException
            If no successful connection could be established with website.

        JsosAuthException
            If user credentials were incorrect.
        """

		tokens = self.__initiate()
		self.__auth(tokens, is_test)
		self.__is_logged = True

	def __initiate(self) -> dict:
		"""Initiates oauth authentication with JSOS"

        Raises
        ------
        JsosConnectionException
            If no successful connection could be established with website.

        """

		login_path = "/index.php/site/loginAsStudent"
		login_url = self.base_jsos_url + login_path
		login_response = self.session.get(login_url)
		if 'url' in login_response.__dict__:
			redirect_url = login_response.url
		else:
			raise JsosConnectionException("No Oauth redirect url.")
		tokens = redirect_url.split('?')[1].split('&')
		return {
			'oauth_token': tokens[0].split('=')[1],
			'oauth_consumer_key': tokens[1].split('=')[1],
			'oauth_locale': tokens[2].split('=')[1]
		}


	def __auth(self, tokens: dict, is_test: bool = False):
		"""Authenticates user with Oauth endpoints of JSOS"

		If the argument `is_test` isn't passed in, connection is checked 10 times. 
        If the argument `is_test` is passed in, connection is checked one time.

        Parameters
        ----------
		tokens : dict
			important tokens used in Oauth requests
		is_test : bool, optional
            is this method used to test connection (default is False)

        Raises
        ------
        JsosConnectionException
            If no successful connection could be established with website.

        """

		data = {
			'id1_hf_0': '',
			'oauth_request_url': f'{self.base_oauth_url}/oauth/authenticate',
			'oauth_consumer_key': tokens['oauth_consumer_key'],
			'oauth_token': tokens['oauth_token'],
			'oauth_locale': tokens['oauth_locale'],
			'oauth_callback_url': f'{self.base_jsos_url}/index.php/site/loginAsStudent',
			'oauth_symbol': 'EIS',
			'username': self.username,
			'password': self.password,
			'authenticateButton': 'Zaloguj'
		}
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		auth_url = self.base_oauth_url + "/oauth/authenticate?0-1.IFormSubmitListener-authenticateForm&" \
			+ 'oauth_token=' + tokens['oauth_token'] + '&' \
			+ 'oauth_consumer_key=' + tokens['oauth_consumer_key'] + '&' \
			+ 'oauth_locale=' + tokens['oauth_locale']

		if is_test:
			tries = 1
		else:
			tries = 10

		for i in range(0, tries):
			auth_resp = self.session.post(auth_url, data, headers)
			if 'message error' in auth_resp.text:
				raise JsosAuthException("Login not successful - check username and/or password")
			elif auth_resp.status_code == 200:
				log.info("Login successful - proceed")
				return
			else:
				log.warning("Login not successful - trying in 10 seconds")
				wait(10)

		raise JsosAuthException(f"Login not successful after {tries} tries - exiting")

	def logout(self, force=False):
		"""Logs user out of JSOS

		If the argument `force` is passed in, clears all class data. 

        Parameters
        ----------
		force : bool, optional
            forces to clear user data (default is False)

        Raises
        ------
        JsosAuthException
            If user is not logged in.

        """

		if not self.__is_logged:
			raise JsosAuthException("User not logged in")
		log.info("Processing logout")
		self.__logout()
		if force:
			self.__clear_data()

	def __logout(self):
		logout_url = self.base_jsos_url + '/index.php/site/logout'
		response = self.session.get(logout_url)
		if response.status_code == 200:
			self.__is_logged = False
			log.info("Logged out successfully")
		else:
			raise JsosAuthException("Cannot log user out")

	def __clear_data(self):
		self.session = None
		self.username = None
		self.password = None
		log.info("User data cleared")

	def is_user_exists(self):
		"""Checks whether user exists"""

		try:
			self.login()
			self.logout()
			return True
		except JsosException:
			log.warning('Wrong username and/or password')
			return False

	def get_messages(self, only_unread: bool = True, max: int = 3) -> list:
		"""Gets messages from JSOS

		If the argument `only_unread` is passed in, looks for unread messages. 
		If the argument `max` is passed in, looks for `max` messages. 

        Parameters
        ----------
		only_unread : bool, optional
            tells whether to look for unread messages or not (default is False)
		max : int, optional
            how many messages to retrieve (default is 3)

        Raises
        ------
        JsosAuthException
            If user is not logged in.

        """

		if not self.__is_logged:
			raise JsosAuthException("User not logged in")

		messages_url = self.base_jsos_url + '/index.php/student/wiadomosci'
		response = self.session.get(messages_url)
		soup = BeautifulSoup(response.text, 'html.parser')
		messages_table = soup.find(class_='table-mailbox')
		if not messages_table:
			log.warning("Probably logged out from JSOS - logging in again")
			self.login()
			return []

		if only_unread:
			if self.has_unread_messages(messages_table=messages_table):
				message_trs = messages_table.find_all(class_='unread')[:max+1]
			else:
				log.info("No new messages")
				return []
		else:
			message_trs = soup.find_all('tr')[1:max+1]

		messages = []
		for tr in message_trs:
			message_url = self.base_jsos_url + tr.attrs['data-url']
			message = dict()
			message_tds = tr.find_all('td')
			message['from'] = message_tds[1].contents[0]
			message['topic'] = message_tds[2].contents[0]
			message['date'] = message_tds[3].contents[0]
			message['html_content'] = self.__get_message_content(message_url)
			messages.append(message)	

		return messages

	def __get_message_content(self, url: str) -> str:
		response = self.session.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		webpage_content = soup.find(id='content').contents[1]
		message_body = webpage_content.find_all('div')[-1]
		message_body_string = str(message_body)

		# Delete unnecessary headers from text
		message_body_string = message_body_string.replace('Message content', '<b>Original message content:</b>')
		message_body_string = message_body_string.replace('Treść wiadomości', '<b>Originalna treść wiadomości:</b>')
		
		return message_body_string
		
	def has_unread_messages(self, messages_table=None):
		"""Checks whether user has unread messages

		If the argument `messages_table` is passed in, looks for messages in given htmls. 

        Parameters
        ----------
		messages_table : html, optional
            messages will be search in it (default is False)
		
        Raises
        ------
        JsosAuthException
            If user is not logged in.

        """
		if not self.__is_logged:
			raise JsosAuthException("User not logged in")

		if messages_table is None:
			messages_url = self.base_jsos_url + '/index.php/student/wiadomosci'
			response = self.session.get(messages_url)
			soup = BeautifulSoup(response.text, 'html.parser')
			messages_table = soup.find(class_='table-mailbox')

		unread_messages = messages_table.find_all(class_='unread')
		if len(unread_messages) == 0:
			return False
		else:
			return True


class JsosException(Exception):
	pass

class JsosConnectionException(JsosException):
	pass

class JsosAuthException(JsosException):
	pass
