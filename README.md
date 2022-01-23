# Jsos2Email

Simple python wrapper for JSOS website and student's mail at WUST

[![Linting](https://github.com/TheArqsz/Jsos2Email/actions/workflows/linting.yml/badge.svg?branch=master)](https://github.com/TheArqsz/Jsos2Email/actions)
[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue?style=flat&logo=python)](https://www.python.org/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

## Installation

```bash
python3 -m venv .venv
python -m pip install -r requirements.txt
```

## Example usage

Script `jsos2mail.py` is designed to be plug-and-go - you just simply run it in your terminal.

```bash
python jsos2email.py --input
```

### Arguments

There are several arguments necessary for the script to run:

- `--wait-time` - wait time between message checking (default: 240s)
- `--input` - lets you type your credentials securely in terminal
- `--useenv` - sets script to use creds from environmental variables:
    - `EMAIL_USERNAME`
    - `EMAIL_PASSWORD`
    - `JSOS_USERNAME`
    - `JSOS_PASSWORD`
- `--no-input` - exact oposite - you have to provide a couple more arguments:
    - `--jsos-usr` - jsos username
    - `--jsos-pwd` - jsos password
    - `--email` - your email
    - `--email-pwd` - your email's password


## Detailed usage

### jsos.Jsos

This class wrapps all connections to JSOS so anyone can access theirs data with python.

#### Usage

To simply connect to JSOS just use:

```python3
from jsos import Jsos

j = Jsos(username=YOUR_USERNAME, password=YOUR_PASSWORD)
j.login()
```

From now you are authenticated and ready to collect messages from JSOS with:

```python3
j.get_messages() -> list
```

To log out simply use:

```python3
j.logout()
```

#### Context

Preferable way to use this wrapper is with the `with` keyword:

```python3
with Jsos(username=YOUR_USERNAME, password=YOUR_PASSWORD) as jsos:
    jsos.get_messages()
```

This way, you are sure that at start you are logged in and after exit you are logged out and all your local data is cleared.

### studentmail.StudentMail

This class wrapps a few connections to student's email server.

#### Usage

To simply connect to email just use:

```python3
from studentmail import StudentMail

s = StudentMail(email=YOUR_EMAIL, password=YOUR_PASSWORD)
s.setup_tls()
```

From now you are authenticated and ready to send messages with your WUST account. 

To do it you need to properly configure message:

- Prepare html-formatted content:

```python3
html_content = """
<div>
    TEST
</div>
"""
```

- Prepare necessary objects:

```python3
s.prepare_message()
s.prepare_headers(subject=SUBJECT_OF_MESSAGE)
s.prepare_content(content=html_content, msg_from=FROM_WHOM_IS_THE_MESSAGE)
```

> Without them, message cannot be sent properly.

Now you are ready to sent your message with:

```python3
s.send()
```

Do not forget to quit server connection after sending message:

```python3
s.quit()
```

#### Context

Preferable way to use this wrapper is with the `with` keyword:

```python3
with StudentMail(email=YOUR_EMAIL, password=YOUR_PASSWORD) as mail:
    mail.prepare_message()
    mail.prepare_headers(subject=SUBJECT_OF_MESSAGE)
    mail.prepare_content(content=html_content, msg_from=FROM_WHOM_IS_THE_MESSAGE)
```

This way, you can be sure that you are authenticated at start and after exit you quited server and all your local data is cleared.
