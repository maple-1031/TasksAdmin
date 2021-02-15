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
import os
from pathlib import Path
import sys
import shutil
import glob

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
    
class Task():
    def __init__(self):
        self.id = 0
        self.path = ""
        self.subject = ""
        self.deadline = 0
        
    def id_gen(self, data):
        return int(data)+1
    
def getLatestDownloadedFileName(arg):
    p = Path(arg)
    files = list(p.glob("*"))
    file_updates = {file_path: os.stat(file_path).st_mtime for file_path in files}

    newst_file_path = max(file_updates, key=file_updates.get)
    return newst_file_path


def dup_check(filename):
    comm = f"select * from files where file='{filename}'"
    if len(tuple(c.execute(comm))) == 0:
        c.execute(f'insert into files values("{filename}")')
        return False
    else:
        return True

mail = settings.user
password = settings.password

downloadsFilePath = r'D:\Users\maple\OneDrive - keio.jp\★課題★\.temp'

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

report_list = []

for i in range(len(report_button)):
    report_temp = []
    report_button = driver.find_elements_by_xpath("//form[@action=\"/ess2/reportAction\"]/button")
    report_subid = driver.find_elements_by_xpath("//form[@action=\"/ess2/reportAction\"]/input[@name=\"SELECT_ENTNO\"]")
    report = Report()
    argid = int(report_subid[i].get_attribute("value"))
    report.name = report.subid2name(argid)
    report_button[i].click()
    report.deadline = driver.find_element_by_xpath('//*[@id="student"]/div[2]/div[1]/form/div[1]/div/div/div/div[2]/div[5]/div/p').text
    temp = driver.find_element_by_xpath('//*[@id="student"]/div[2]/div[1]/form/div[1]/div/div/div/div[2]/div[1]/div/p').text

    
    if not dup_check(temp):
        try:
            driver.find_element_by_xpath('//*[@name="BTN__DL"]')
        except:
            report.filename = "#"
        else:
            driver.find_element_by_xpath('//*[@name="BTN__DL"]').click()
            try:
                driver.find_element_by_xpath('//button[@onclick="agreeSubmit("#_DL", "");"]').click()
            except:
                pass
            else:
                pass

            timeout_second = 5

            for i in range(timeout_second + 1):
                download_fileName = glob.glob(f'{downloadsFilePath}\\*.*')

                if download_fileName:
                    extension = os.path.splitext(download_fileName[0])

                    if '.crdownload' not in extension[1] : break

                if i >= timeout_second:
                    driver.quit()
                    shutil.rmtree(downloadsFilePath)
                    sys.exit()

                time.sleep(1)

            report.filename = getLatestDownloadedFileName(downloadsFilePath)
    
    report_temp = [report.name, report.deadline, report.filename]
    report_list.append(report_temp)
    
    driver.find_element_by_xpath('//button[@name="BTN_JIKANWARI"]').click()
    
print(report_list)
conn.close()
driver.quit()

for i in report_list:
    task = Task()
    with open("current_tasks.json") as f:
        df = json.load(f)

    task.path = i[3]
    task.subject = i[0]
    task.deadline = int(task.deadline_gen(i[1]))
    task.deadline_str = i[1]
    task.task_hash = hash("".join(i[:3]))
    temp_dict = {"path":task.path, "subject":task.subject, "deadline_unix":task.deadline, "deadline_str":task.deadline_str, "task_hash":task.task_hash}
    if temp_dict not in list(df.values())[0]:
        df["current_tasks"].append(temp_dict)

    with open("current_tasks.json", "w") as f:
        json.dump(df, f, indent=4)

nc = Flask(__name__)

@nc.route("/")
def check():
      rep_num = {"list": 2}
      deadline = {0: 10, 1 :300}
      subject = {"val1": 5, "val2": 400}
      return render_template('index.html', deadline = deadline, subject = subject, rep_num = rep_num)

if __name__ == '__main__':
    nc.run(host="127.0.0.1", port=8080, debug=False)

