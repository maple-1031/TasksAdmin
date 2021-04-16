# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 17:48:24 2021

@author: maple
"""

from selenium import webdriver
import settings
import time
import json
import datetime as dt

#%%

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
        dl_pre_int = dt.datetime.strptime(dl_str, "%Y-%m-%d %H:%M:%S")
        dl_int = dl_pre_int.timestamp()
        return dl_int
    
def cms_dl(dl_date, dl_time):
    today_date = dt.date.today().weekday()
    en_date = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    jp_date = ["月", "火", "水", "木", "金", "土", "日"]
    if "曜" in list(dl_date):
        date_difference = jp_date.index(dl_date[0]) - today_date
        if date_difference < 0:
            date_difference = 7 + date_difference
            
        dl_day = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + dt.timedelta(days=date_difference) + dt.timedelta(hours=int(dl_time.split(".")[0])) + dt.timedelta(minutes=int(dl_time.split(".")[1]))
    else:
        dl_day = dt.datetime.strptime(f'{dt.date.today():%Y}年' + dl_date + " " +dl_time, "%Y年%m月%d日 %H.%M")
        if dl_day < dt.datetime.now():
            dl_day += dt.timedelta(year=1)
        
    return dl_day.strftime("%Y-%m-%d %H:%M")
        

#%%

prefs = {"download.default_directory" : r"D:\Users\maple\OneDrive - keio.jp\★課題★\.temp"}

mail = settings.user
password = settings.password    

chromeOptions = webdriver.ChromeOptions()
#    chromeOptions.add_argument("--headless")
chromeOptions.add_experimental_option("prefs",prefs)

chrome_path = "D:\\Users\\maple\\Python\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_path, options=chromeOptions)
driver.get('https://lms.keio.jp/')

#%%

login = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[3]/ul/li[1]/h2/a")
login.click()

#%%

time.sleep(1)
search_box = driver.find_element_by_id("username")
search_box.send_keys(mail)
pass_box = driver.find_element_by_id("password")
pass_box.send_keys(password)
submit_bottun = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/form/section[3]/button")
submit_bottun.click()
time.sleep(0.5)
#%%
driver.switch_to.window(driver.window_handles[0])
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        driver.find_element_by_xpath("//span[text()='もっと読み込む']/parent::button").click()
    except:
        pass
    
    # Wait to load page
    time.sleep(2)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

#%%

dash_div_list = driver.find_elements_by_xpath("//div[@class='PlannerItem-styles__type']")
dash_task_list = []

for element in dash_div_list:
    new_element = element.find_element_by_xpath(".//span")
    if new_element.text.split(" ")[-1] == "課題":
        click_element = element.find_element_by_xpath(".//span/parent::div[@class='PlannerItem-styles__type']/following-sibling::div[@class='PlannerItem-styles__title']/a").get_attribute("href")
        dash_task_list.append(click_element)
        print(click_element)

#%%
with open("current_tasks.json", mode="rt", encoding="utf-8") as f:
    df = json.load(f)
    
for url in dash_task_list:
    task = Task()
    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    try:
        driver.find_element_by_xpath("//a[@class='instructure_file_link']").click()
    except:
        pass
    else:
        file_name = driver.find_element_by_xpath("//a[@class='instructure_file_link']").get_attribute("title")
        
    try:
        dl_date = driver.find_element_by_xpath("//span[@class='display_date']").text
    except:
        pass
    else:
        dl_time = driver.find_element_by_xpath("//span[@class='display_time']").text
        
        
        task.path = rf"D:\Users\maple\OneDrive - keio.jp\★課題★\.temp\{file_name}"
        task.subject = driver.find_elements_by_xpath("//span[@class='ellipsible']")[1].text
        task.deadline_str = cms_dl(dl_date, dl_time)
        task.deadline = dt.datetime.strptime(task.deadline_str, "%Y-%m-%d %H:%M").timestamp()
        task.task_hash = str(hash("".join([task.subject, task.deadline_str])))
        driver.close()
        temp_dict = {
            "path":task.path,
            "subject":task.subject,
            "deadline_unix":task.deadline,
            "deadline_str":task.deadline_str,
            "deadline_day_str":task.deadline_str.split(" ")[0],
            "task_hash":task.task_hash,
            "submit_url": url
        }
        
        df["current_tasks"].append(temp_dict)
        df["current_tasks"] = sorted(df["current_tasks"], key=lambda x: x['deadline_unix'])

with open("current_tasks.json", mode="wt", encoding="utf-8") as f:
    json.dump(df, f, indent=4, ensure_ascii=False)

driver.quit()