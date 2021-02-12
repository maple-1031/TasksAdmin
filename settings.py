# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 08:23:13 2021

@author: maple
"""

import os
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

user = os.environ.get("KEIO-USER")
password = os.environ.get("KEIO-PASS")