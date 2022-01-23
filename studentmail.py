#!/usr/bin/env python3

"""Wrapper for WUST student's mail sender

This class allows to connect to student's mail and send messages.
"""

__author__ = 'Arqsz'

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import logging
import smtplib
import config  # noqa: F401

log = logging.getLogger('jsos2mail')


class StudentMail:
    """
    Class that allows to send emails to pwr.edu.pl domain.

    Attributes
    ----------
    email : str
        the email address of the user
    password : str
        the password for given email account
    server_host : str, optional
        host of email smtp server
    port : int, optional
        port of email smtp server

    Methods
    -------
    setup_tls()
        Starts TLS connection to server
    quit()
        Ends connection to server
    prepare_message(message=None)
        Creates basic MIMEMultipart message
    prepare_headers(subject='', msg_from='jsos_bot@pwr.edu.pl')
        Prepares headers for MIMEMultipart message
    prepare_content(content, msg_from='jsos_bot@pwr.edu.pl')
        Adds html content to MIMEMultipart message
    send(receiver=None)
        Sends message to receiver
    """

    def __init__(
            self, email: str,
            password: str, server_host: str = 'smtp.gmail.com',
            port: int = 587
    ):
        self.email = email
        self.password = password
        self.server_host = server_host
        self.port = port
        self.server = smtplib.SMTP(host=self.server_host, port=self.port)
        self.message = None
        self.__headers_prepared = False

    def __enter__(self):
        self.setup_tls()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.quit()

    def setup_tls(self):
        """Starts TLS connection to server.

        Raises
        ------
        SMTPAuthenticationError
            If no successful connection could be established with server.

        """

        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.email, self.password)

    def quit(self):
        """Ends connection to server

        Raises
        ------
        SMTPAuthenticationError
            If no successful connection could be established with server.

        """

        self.server.quit()

    def prepare_message(self, message: MIMEMultipart = None):
        """Creates basic MIMEMultipart message

        Parameters
        ----------
        message : MIMEMultipart, optional
                        message object (default is None)

        """

        if not message:
            self.message = MIMEMultipart("alternative")
        else:
            self.message = message

    def prepare_headers(
            self,
            subject: str = '',
            msg_from: str = 'jsos_bot@pwr.edu.pl'
    ):
        """Prepares headers for MIMEMultipart message

        Parameters
        ----------
        subject : str, optional
            subject of message (default is '')
        msg_from : str, optional
            from whom message was sent (default is 'jsos_bot@pwr.edu.pl')

        Raises
        ------
        StudentMailException
            If message is not prepared

        """

        if not self.message:
            raise StudentMailException("Message not prepared")
        self.message["Subject"] = subject
        self.message["From"] = msg_from
        self.message["To"] = self.email
        self.__headers_prepared = True

    def prepare_content(
            self,
            content: str,
            msg_from: str = 'jsos_bot@pwr.edu.pl'
    ):
        """Adds html content to MIMEMultipart message

        Parameters
        ----------
        content : str
            html content of message
        msg_from : str, optional
            from whom message was sent (default is 'jsos_bot@pwr.edu.pl')

        Raises
        ------
        StudentMailException
            If message is not prepared

        """

        if not self.message:
            raise StudentMailException("Message not prepared")
        elif not self.__headers_prepared:
            raise StudentMailException("Headers not prepared")

        html = """
        From: <b>{}</b>
        <br/>
        <br/>
        {}
        """.format(msg_from, content)
        part = MIMEText(html, "html")
        self.message.attach(part)

    def send(self, receiver: str = None):
        """Sends message to receiver

        If `receiver` is not set, user's mail is being choosen.

        Parameters
        ----------
        receiver : str, optional
            receiver of message (default is None)

        Raises
        ------
        StudentMailException
            If message is not prepared

        """
        if not self.message:
            raise StudentMailException("Message not prepared")
        elif not self.__headers_prepared:
            raise StudentMailException("Headers not prepared")

        if not receiver:
            receiver = self.email

        self.server.sendmail(
            self.email, receiver, self.message.as_string()
        )

    def is_user_exists(self):
        """Checks whether user exists"""

        try:
            self.setup_tls()
            self.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            self.quit()
            log.warning('Wrong username and/or password')
            return False


class StudentMailException(Exception):
    pass
