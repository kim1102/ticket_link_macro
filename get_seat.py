"""
written by dev.kim
bug report: devkim1102@gmail.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from config import conf
import multiprocessing
import time

class ssiba_ticket():
    def __init__(self):
        self.ticket_url = conf['ticket_url']
        self.ticket_link_url = conf['root_url']
        self.naver_time_url = conf['naver_time']
        self.target_time = conf['target_time']
        self.target_min = conf['target_min']
        self.target_sec = conf['target_sec']
        self.refresh_xpath = '//*[@id="container"]/div[1]/div[2]/div[2]/div[1]/div[2]/a'

    def initilize_driver(self):
        options1 = webdriver.ChromeOptions()
        options2= webdriver.ChromeOptions()

        # ticket URL
        options1.add_argument('--start-maximized')
        driver1 = webdriver.Chrome('chromedriver.exe', options=options1)
        driver1.get(url=self.ticket_url)
        driver1.implicitly_wait(time_to_wait=10)

        # # naver closk
        # options2.add_argument('--window-size=500,500')
        # driver2 = webdriver.Chrome('chromedriver.exe', options=options2)
        # driver2.get(url=self.naver_time_url)
        # driver2.implicitly_wait(time_to_wait=2)

        self.driver1 = driver1
        # self.driver2 = driver2

    def wait_until_login(self):
        while True:
            try:
                if self.driver1.current_url == self.ticket_link_url:
                    break
            except:
                pass
        self.driver1.get(url=self.ticket_url)
        self.driver1.implicitly_wait(time_to_wait=5)

        # wait until captcha done...
        time.sleep(15)

        self.refresh_btn = \
            self.driver1.find_elements(by=By.XPATH, value=self.refresh_xpath)


    def refresh_on_target_time(self):
        while True:
            try:
                current_time = self.driver2.find_element(by=By.CSS_SELECTOR, value=
                    '#_cs_domestic_clock > div._timeLayer.time_bx > div > div').text
                current_time = current_time.split('\n')
                cur_h = current_time[0] + current_time[1]
                cur_m = current_time[3] + current_time[4]
                cur_s = current_time[6] + current_time[7]

                if cur_h == self.target_time and cur_m == self.target_min and cur_s == self.target_sec:
                    self.driver1.refresh()
                    break
            except:
                pass

    def wait_until_empty_seat_exists(self):
        while True:
            self.refresh_btn[0].click()

            R_seat = self.driver1.find_element(by=By.XPATH,
                                               value='/html/body/div/div[2]/div[1]/div[2]/div[2]/ul/li[2]/a/div/span[3]/span[1]').text
            S_seat = self.driver1.find_element(by=By.XPATH,
                                               value='/html/body/div/div[2]/div[1]/div[2]/div[2]/ul/li[3]/a/div/span[3]/span[1]').text

            if R_seat != '0' or S_seat != '0':
                break
            else:
                time.sleep(0.05)


if __name__ == '__main__':
    ticket_bot = ssiba_ticket()

    # url & driver initialize
    ticket_bot.initilize_driver()
    ticket_bot.wait_until_login()
    ticket_bot.wait_until_empty_seat_exists()



