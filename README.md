# jsos2mail

Simple python wrapper for JSOS website and student's mail at WUST

## Installation

```bash
python3 -m pip install -r requirements.txt
```
## jsos.Jsos

This class wrapps all connections to JSOS so anyone can access theirs data with python.

### Simple usage

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

### Context usage

Preferable way to use this wrapper is with the `with` keyword:

```python3
with Jsos(username=YOUR_USERNAME, password=YOUR_PASSWORD) as jsos:
    jsos.get_messages()
```

This way, you are sure that at start you are logged in and after exit you are logged out and all your local data is cleared.

## mail.StudentMail

This class wrapps a few connections to student's email server.

### Simple usage

To simply connect to email just use:

```python3
from mail import StudentMail

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

### Context usage

Preferable way to use this wrapper is with the `with` keyword:

```python3
with StudentMail(email=YOUR_EMAIL, password=YOUR_PASSWORD) as mail:
    mail.prepare_message()
    mail.prepare_headers(subject=SUBJECT_OF_MESSAGE)
    mail.prepare_content(content=html_content, msg_from=FROM_WHOM_IS_THE_MESSAGE)
```

This way, you can be sure that you are authenticated at start and after exit you quited server and all your local data is cleared.

## Example usage

Script `run.py` is designed to be plug-and-go - you just simply run it in your terminal.

### Arguments

There are several arguments necessary for the script to run:

- `--wait-time` - wait time between message checking (default: 240s)
- `--input` - lets you type your credentials securely in terminal
- `--no-input` - exact oposite - you have to provide a couple more arguments:

    - `--jsos-usr` - jsos username
    - `--jsos-pwd` - jsos password
    - `--email` - your email
    - `--email-pwd` - your email's password


