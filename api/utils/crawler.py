import time, os
import logging
from typing import Optional
import pandas as pd

from io import TextIOWrapper
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

search_key = "광화문 카페"

# 크롬 드라이버 실행
class CrawlerNaverMap:
  def __init__(self) -> None:
    pass

  def get_driver(self):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664 Safari/537.36") 
    options.add_argument("window-size=1440x900")
    # 브라우저가 백그라운드에서 실행됩니다.
    # options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # chromedriver 열기
    driver.get('https://map.naver.com')
    print("got driver")
    driver.implicitly_wait(60)
    return driver

  # 검색어 입력
  def search_place(self,driver:WebDriver, search_text: str):
    search_input_box = driver.find_element(By.CSS_SELECTOR,"div.input_box>input.input_search")
    search_input_box.send_keys(search_text)
    search_input_box.send_keys(Keys.ENTER)
    time.sleep(5)

  # 다음 페이지 이동 및 마지막 페이지 검사
  def next_page_move(self,driver:WebDriver):
    # 페이지네이션 영역에 마지막 버튼 선택
    #! ToDo : next page element 교체
    next_page_btn = driver.find_element(By.CSS_SELECTOR,'div._2ky45>a:last-child')
    next_page_class_name = BeautifulSoup(next_page_btn.get_attribute('class'), "html.parser")

    if len(next_page_class_name.text) > 10:
      print("검색완료")
      driver.quit()
      return False
    else:
      next_page_btn.send_keys(Keys.ENTER)
      return True

  # 검색 iframe 이동
  def to_search_iframe(self,driver:WebDriver):
    driver.switch_to.default_content()
    driver.switch_to.frame('searchIframe')

  # element 텍스트 추출
  def get_element_to_text(self,element):
    return BeautifulSoup(element, "html.parser").get_text()

  # 매장정보 추출
  def get_store_data(self,driver:WebDriver, scroll_container: WebElement)-> dict:
    result_dict = {}
    get_store_li = scroll_container.find_elements(By.CSS_SELECTOR,'ul > li')
    print("get_store_li len: ", len(get_store_li))

    for index in range(len(get_store_li)):
      selectorArgument = 'div:nth-of-type(1) > a'

      # 매장 항목 클릭
      get_store_li[index].find_element(By.CSS_SELECTOR,selectorArgument).click()

      # 매장 상세로 iframe 이동
      driver.switch_to.default_content()
      driver.switch_to.frame('entryIframe')

      time.sleep(1)

      try:
        try: 
          WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, "place_didmount")))
        except TimeoutException:
          self.to_search_iframe(driver)

        store_name = self.get_element_to_text(driver.find_element(By.CSS_SELECTOR,'#_title > span:nth-child(1)').get_attribute('innerHTML'))
        store_type = self.get_element_to_text(driver.find_element(By.CSS_SELECTOR,'#_title > span:nth-child(2)').get_attribute('innerHTML'))
        c_time = self.get_element_to_text(driver.find_element(By.CSS_SELECTOR, 'time').get_attribute('innerHTML'))

        time_itself = c_time[:5]
        time_content = c_time[-5:]
        result_dict[store_name] = {"type" : store_type,"time" : time_itself, "content" : time_content}
        
        self.to_search_iframe(driver)
      except TimeoutException:
        self.to_search_iframe(driver)
    return result_dict

 
  def main(self, search_keyword : Optional[str] = search_key)->dict:
    driver = self.get_driver()
    print(driver)
    self.search_place(driver,search_keyword)
    self.to_search_iframe(driver)
    time.sleep(2)

    try:
      scroll_container = driver.find_element(By.ID,"_pcmap_list_scroll_container")
    except:
      print("스크롤 영역 감지 실패")

    try:
      while True:
        for i in range(6):
          # 자바 스크립트 실행
          driver.execute_script("arguments[0].scrollBy(0,2000)",scroll_container)
          time.sleep(0.5)
        res = self.get_store_data(driver,scroll_container)
        print(res)
        is_continue = self.next_page_move(driver)
        print("nextpage")
        if is_continue == False:
          break
      return res
    except:
      print("크롤링 과정 중 에러 발생")
      return res

if __name__ =="__main__":
  crw = CrawlerNaverMap()
  crw.main("광장동 카페")