# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 22:48:13 2020

@author: maple
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from flask import Flask, redirect ,request,render_template,jsonify, Response
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
from datetime import datetime as dt
import importlib

import settings
importlib.reload(settings)


class Report():
    def __init__(self):
        self.name = ""
        self.deadline = ""
        self.filename = ""
        self.reportname = ""

    def subid2name(self, subid):
        comm = f"select * from subs where subid = {subid}"
        i = tuple(c.execute(comm))
        return i[0][1]

class Task():
    def __init__(self):
        self.path = ""
        self.subject = ""
        self.deadline = 0
        self.deadline_str = ""
        self.task_hash = ""

    def id_gen(self, data):
        return int(data)+1

    def deadline_gen(self, dl_str):
        dl_pre_int = dt.strptime(dl_str, "%Y-%m-%d %H:%M:%S")
        dl_int = dl_pre_int.timestamp()
        return dl_int

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

 

nc = Flask(__name__)

@nc.route("/")
def check():
    conn = sqlite3.connect('subs_2020.db')
    global c
    c = conn.cursor()
    
    prefs = {"download.default_directory" : r"D:\Users\maple\OneDrive - keio.jp\★課題★\.temp"}
    
    mail = settings.user
    password = settings.password    
    
    chromeOptions = webdriver.ChromeOptions()
#    chromeOptions.add_argument("--headless")
    chromeOptions.add_experimental_option("prefs",prefs)
    
    downloadsFilePath = r'D:\Users\maple\OneDrive - keio.jp\★課題★\.temp'
    
    with open("recent_refresh.json") as f:
        recent_refresh = json.load(f)
    
    now = dt.now()
    recent_refresh_time = dt.strptime(recent_refresh["recent_refresh"], "%Y-%m-%d %H:%M:%S")
    
    if (now - recent_refresh_time).total_seconds() > 3600:
        
        with open("recent_refresh.json") as f:
            ref_dic = json.load(f)
            
        ref_dic["recent_refresh"] = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open("recent_refresh.json", "w") as f:
            json.dump(ref_dic, f, indent=4)
                
        chrome_path = "D:\\Users\\maple\\Python\\chromedriver_win32\\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_path, options=chromeOptions)
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
            report.reportname = temp
        
            report_temp = [report.name, report.deadline, report.reportname, report.filename]
            report_list.append(report_temp)
        
            driver.find_element_by_xpath('//button[@name="BTN_JIKANWARI"]').click()
        
        conn.commit()
        conn.close()
        driver.quit()
        
        for i in report_list:
            task = Task()
            with open("current_tasks.json", mode="rt", encoding="utf-8") as f:
                df = json.load(f)
                
        
            task.path = i[3]
            task.subject = i[0]
            task.deadline = int(task.deadline_gen(i[1]))
            task.deadline_str = i[1]
            task.task_hash = str(hash("".join(i[:3])))
            temp_dict = {"path":task.path,
                         "subject":task.subject,
                         "deadline_unix":task.deadline,
                         "deadline_str":task.deadline_str,
                         "deadline_day_str":task.deadline_str.split(" ")[0],
                         "task_hash":task.task_hash
                         }
            if temp_dict not in list(df.values())[0]:
                df["current_tasks"].append(temp_dict)
        
            with open("current_tasks.json", mode="wt", encoding="utf-8") as f:
                json.dump(df, f, indent=4, ensure_ascii=False)

            df["current_tasks"] = sorted(df["current_tasks"], key=lambda x: x['deadline_unix'])

        
        #ここまで
    
    with open("current_tasks.json", mode="rt", encoding="utf-8") as f:
        current_tasks = json.load(f)
    
    return render_template('index.html', ct = current_tasks, rep_num = len(current_tasks["current_tasks"]))

@nc.route("/", methods=["POST"])
def post():
    task = Task()
    submit_task_name = request.form.get("new-task-name")
    submit_task_deadline = request.form.get("new-task-deadline")
    submit_task_deadline_str = " ".join(submit_task_deadline.split("T"))
    submit_task_deadline = int(task.deadline_gen(" ".join(submit_task_deadline.split("T")) + ":00"))
    submit_task_file = request.files.get("new-task-file")
    
    task.path = r"D:\Users\maple\OneDrive - keio.jp\★課題★\.temp"
    task.subject = submit_task_name
    task.deadline = submit_task_deadline
    task.deadline_str = submit_task_deadline_str
    task.task_hash = str(hash("".join([task.subject, task.deadline_str])))
    temp_dict = {
        "path":task.path,
        "subject":task.subject,
        "deadline_unix":task.deadline,
        "deadline_str":task.deadline_str,
        "deadline_day_str":task.deadline_str.split(" ")[0],
        "task_hash":task.task_hash
        }
    
    with open("current_tasks.json", mode="rt", encoding="utf-8") as f:
        df = json.load(f)
    df["current_tasks"].append(temp_dict)
    df["current_tasks"] = sorted(df["current_tasks"], key=lambda x: x['deadline_unix'])
    
    with open("current_tasks.json", mode="wt", encoding="utf-8") as f:
        json.dump(df, f, indent=4, ensure_ascii=False)
        
    with open("current_tasks.json", mode="rt", encoding="utf-8") as f:
        current_tasks = json.load(f)
        
    return render_template('index.html', ct = current_tasks, rep_num = len(current_tasks["current_tasks"]))

@nc.route("/delete", methods = ["POST"])
def delete():
    delete_hash = request.form.get("delete_hash")
    with open("current_tasks.json", mode="rt", encoding="utf-8") as f:
        df = json.load(f)
        hash_list = [d.get("task_hash") for d in df["current_tasks"]]
        hash_index = hash_list.index(delete_hash)
        df["current_tasks"].pop(hash_index)
        df["current_tasks"] = sorted(df["current_tasks"], key=lambda x: x['deadline_unix'])

    
    with open("current_tasks.json", mode="wt", encoding="utf-8") as f:
        json.dump(df, f, indent=4, ensure_ascii=False)
        
    with open("current_tasks.json", mode="rt", encoding="utf-8") as f:
        current_tasks = json.load(f)
        
    return redirect("/")

if __name__ == '__main__':
    nc.run(host="0.0.0.0", port=8080, debug=False)
