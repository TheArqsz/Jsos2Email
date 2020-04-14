#!/usr/bin/env python3

"""Config file for json and mail modules"""

__author__ = "Arqsz"

import logging
log = logging.Logger("jsos2mail")
logging.basicConfig(
			level=logging.INFO, 
			format='[%(asctime)s] %(module)s: %(message)s', 
			datefmt='%m/%d/%Y %H:%M:%S'
		)