#!/usr/bin/env python3

"""Config file for json and mail modules"""

__author__ = "Arqsz"

import logging
from time import time

log = logging.Logger("jsos2mail")
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] (%(filename)s:%(lineno)d) %(levelname)-8s %(name)s: %(message)s',  # noqa: E251,E501
    datefmt='%m/%d/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler(f"jsos2mail-{int(time())}.log"),
        logging.StreamHandler()
    ]
)
