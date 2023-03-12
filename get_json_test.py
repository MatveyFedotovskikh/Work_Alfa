import functools
import time
from typing import KeysView
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import password 
import json
import requests


class Selenium_test():
    def __init__(self):
        options = webdriver.ChromeOptions()
        # user-agent
        options.add_argument('user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0')
        options.add_argument('log-level=INT')
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            executable_path=password.path_sel,
            options=options
        )
        self.date_now = 2 #datetime.datetime.now().month
        self.data = {}
        self.run = True
        self.error = 0

    def start(self,link_alfa):
        self.driver.get(link_alfa)
        time.sleep(1)
        email_input = self.driver.find_element(by=By.ID, value="loginform-username")
        email_input.clear()
        email_input.send_keys(password.login_alfa)
        time.sleep(0.2)
        password_input = self.driver.find_element(by=By.ID, value="loginform-password")
        password_input.clear()
        password_input.send_keys(password.passowrd_alfa)
        time.sleep(0.2)
        password_input.send_keys(Keys.ENTER)
        time.sleep(1) 

    def return_data_json(self):
        data = json.loads(self.driver.find_element(by=By.XPATH, value=f'/html/body/pre').text)
        return data 
    
def main():
    link_alfa = 'https://rtschool.s20.online/company/1/calendar-teacher/calendar-fetch?start=2023-03-10&end=2023-03-11&_=1678474677305'
    selenium = Selenium_test()
    selenium.start(link_alfa)
    data_end = selenium.return_data_json()

main()
