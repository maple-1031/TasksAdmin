# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 14:52:22 2021

@author: maple
"""

from selenium import webdriver
import settings
import time
import json


prefs = {"download.default_directory" : r"D:\Users\maple\OneDrive - keio.jp\★課題★\.temp"}

mail = settings.user
password = settings.password    

chromeOptions = webdriver.ChromeOptions()
#    chromeOptions.add_argument("--headless")
chromeOptions.add_experimental_option("prefs",prefs)

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

btn_list = driver.find_elements_by_xpath("//form[@action='/ess2/timeTable']")

btn_list = btn_list[3:-1]

half = (len(btn_list)//3)
btn_list = btn_list[half*2:]

class Subject():
    def __init__(self):
        self.name = ""
        self.lecturer = ""
        self.id = 0
        self.weekday = 0
        self.period = 0
        self.cms_url = ""

with open("current_subs.json", mode="rt", encoding="utf-8") as f:
    df = json.load(f)

for element in btn_list:
    subject = Subject()
    subject.name = element.find_element_by_xpath(".//button").get_attribute("textContent")
    subject.lecturer = ""
    subject.id = element.find_element_by_xpath(".//input[@name='SELECT_ENTNO']").get_attribute("value")
    subject.weekday = element.find_element_by_xpath(".//input[@name='SELECT_WD']").get_attribute("value")
    subject.period = element.find_element_by_xpath(".//input[@name='SELECT_COL']").get_attribute("value")
    try:
        subject.cms_url = element.find_element_by_xpath(".//button/parent::form/following-sibling::div[@class='lms-wrap']/a").get_attribute("href")
    except:
        subject.cms_url = "#"
    
    temp_dic = {
            "name":subject.name,
            "lecturer":subject.lecturer,
            "id":subject.id,
            "weekday":subject.weekday,
            "period":subject.period,
            "cms_url":subject.cms_url
        }
    df.append(temp_dic)
    
with open("current_subs.json", mode="wt", encoding="utf-8") as f:
    json.dump(df, f, indent=4, ensure_ascii=False)