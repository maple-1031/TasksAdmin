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
import time
from selenium import webdriver
import sqlite3

import settings

conn = sqlite3.connect('subs_2020.db')
c = conn.cursor()

class Report():
    def __init__(self):
        self.name = ""
        self.deadline = ""
        self.filepass = ""
        
    def subid2name(self, subid):
        comm = f"select * from subs where subid = {subid}"
        i = tuple(c.execute(comm))
        return i[0][1]

mail = settings.user
password = settings.password

driver = webdriver.Chrome("D:\\Users\\maple\\Python\\chromedriver_win32\\chromedriver.exe")
driver.get('https://portal.keio.jp/koid/')
time.sleep(1)
search_box = driver.find_element_by_id("username")
search_box.send_keys(mail)
pass_box = driver.find_element_by_id("password")
pass_box.send_keys(password)
submit_bottun = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/form/section[3]/button")
submit_bottun.click()
time.sleep(0.5)

seminor_botton = driver.find_element_by_id("ui-id-12")
seminor_botton.click()

seminor_suport_button = driver.find_element_by_id("ui-id-51")
seminor_suport_button.click()

driver.switch_to.window(driver.window_handles[1])
time.sleep(0.5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(0.5)

report_button = driver.find_elements_by_xpath("//form[@action=\"/ess2/reportAction\"]/button")
report_subid = driver.find_elements_by_xpath("//form[@action=\"/ess2/reportAction\"]/input[@name=\"SELECT_ENTNO\"]")

nc = Flask(__name__)

@nc.route("/")
def check():
      rep_num = {"list": 6}
      deadline = {0: 10, 1 :200}
      subject = {"val1": 5, "val2": 400}
      return render_template('index.html', deadline = deadline, subject = subject, rep_num = rep_num)

if __name__ == '__main__':
    nc.run(host="127.0.0.1", port=8080)

