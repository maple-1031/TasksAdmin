# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 22:48:13 2020

@author: maple
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from flask import Flask, redirect ,request,render_template,jsonify
from flask_bootstrap import Bootstrap
import json
import requests

nc = Flask(__name__)

@nc.route("/")
def check():
      rep_num = {"list": 20}
      deadline = {0: 10, 1 :200}
      subject = {"val1": 5, "val2": 400}
      return render_template('index.html', deadline = deadline, subject = subject, rep_num = rep_num)

if __name__ == '__main__':
    nc.run(host="127.0.0.1", port=8080)
    