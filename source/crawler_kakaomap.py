# 25개구 for문으로 돌려서 카페 정보 크롤링하기

import os
from time import sleep
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils import utils
##########################################################################
##################### variable related selenium ##########################
##########################################################################
# 서울 특별시 구 리스트
# gu_list = ['마포구','서대문구','은평구','종로구','중구','용산구','성동구','광진구',
#            '동대문구','성북구','강북구','도봉구','노원구','중랑구','강동구','송파구',
#            '강남구','서초구','관악구','동작구','영등포구','금천구','구로구','양천구','강서구']

gu_list =gu_list = ['서대문구 신촌동']
# csv 파일에 헤더 만들어 주기

def main1():
    fileName = './res/requested.csv'
    file = open(fileName, 'w', encoding='utf-8')
    file.write("카페명" + "," + "주소" + "," + "영업시간" + "," + "전화번호"+"\n")
    file.close()

    for index, gu_name in enumerate(gu_list):
        # fileName = './res/' + index.__str__() + '_' + gu_name + '.'+'csv'
        # file = open(fileName, 'w', encoding='utf-8')
        # file.write("카페명" + "|" + "주소" + "|" + "영업시간" + "|" + "전화번호"+"\n")
        # file.close()                                    # 처음에 csv파일에 칼럼명 만들어주기
        
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36   ")
        options.add_argument('lang=ko_KR')
        options.add_argument("headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        driver.get('https://map.kakao.com/')  # 주소 가져오기
        search_area = driver.find_element(By.XPATH,'//*[@id="search.keyword.query"]') # 검색 창
        search_area.send_keys(gu_name + ' 카페')  # 검색어 입력
        driver.find_element(By.XPATH,'//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
        driver.implicitly_wait(3) # 기다려 주자
        more_page = driver.find_element(By.ID,"info.search.place.more")
        # more_page.click()
        more_page.send_keys(Keys.ENTER) # 더보기 누르고
        # 첫 번째 검색 페이지 끝
        # driver.implicitly_wait(5) # 기다려 주자
        time.sleep(1)

        # next 사용 가능?
        next_btn = driver.find_element(By.ID,"info.search.page.next")
        has_next = "disabled" not in next_btn.get_attribute("class").split(" ")
        Page = 1
        while has_next: # 다음 페이지가 있으면 loop
        # for i in range(2, 6): # 2, 3, 4, 5
            file = open(fileName, 'a', encoding='utf-8')
            time.sleep(0.5)
            # place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li:nth-child(1)')
            # 페이지 루프
            #info\.search\.page\.no1 ~ .no5
            page_links = driver.find_elements(By.CSS_SELECTOR,"#info\.search\.page a")
            pages = [link for link in page_links if "HIDDEN" not in link.get_attribute("class").split(" ")]
            # print(len(pages), "개의 페이지 있음")
            # pages를 하나씩 클릭하면서
            for i in range(1, 6):
                xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
                try:
                    page = driver.find_element(By.XPATH,xPath)
                    page.send_keys(Keys.ENTER)
                except: 
                    print('End of Page')
                    break
                sleep(3)
                place_lists = driver.find_elements(By.CSS_SELECTOR,'#info\.search\.place\.list > li')
                for p in place_lists: # WebElement
                    # print(p.get_attribute('innerHTML'))
                    # print("type of p:", type(p))
                    store_html = p.get_attribute('innerHTML')
                    store_info = BeautifulSoup(store_html, "html.parser")
                    # BS -> 분석
                    #
                    place_name = store_info.select('.head_item > .tit_name > .link_name')
                    if len(place_name) == 0:
                        continue # 광고
                    place_name = store_info.select('.head_item > .tit_name > .link_name')[0].text
                    if ',' in place_name:
                        place_name = place_name.replace(',','&')
                    place_address = store_info.select('.info_item > .addr > p')[0].text
                    if ',' in place_address:
                        place_address = place_address.replace(',','&')
                    place_hour = store_info.select('.info_item > .openhour > p > a')[0].text
                    if ',' in place_hour:
                        place_hour = place_hour.replace(',','&')
                    place_tel = store_info.select('.info_item > .contact > span')[0].text

                    driver.switch_to.window(driver.window_handles[0])

                    file.write(place_name + "," + place_address + "," + place_hour + "," + place_tel + "\n")
                print(i, ' of', ' [ ' , Page, ' ] ')
            next_btn = driver.find_element(By.ID,"info.search.page.next")
            has_next = "disabled" not in next_btn.get_attribute("class").split(" ")
            if not has_next:
                print('Arrow is Disabled')
                driver.close()
                file.close()
                break # 다음 페이지 없으니까 종료
            else: # 다음 페이지 있으면
                Page += 1
                next_btn.send_keys(Keys.ENTER)
        print("End of Crawl")
        driver.quit()

def main2():
    fileName = './res/requested.csv'
    df = pd.read_csv(fileName, encoding='utf-8',sep=",")
    current = utils.get_time()
    for times in df['영업시간']:
        if len(times)>4:
            closing_time = times[-5:]



if __name__=="__main__":
    # main1()
    main2()