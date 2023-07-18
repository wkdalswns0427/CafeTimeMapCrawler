import pandas as pd # 표 형식의 데이터를 다룰 수 있는 pandas를 pd라고 줄여서 불러옵니다
from selenium import webdriver # 크롬 창을 조종하기 위한 모듈입니다
from selenium.webdriver.common.by import By # 웹사이트의 구성요소를 선택하기 위해 By 모듈을 불려옵니다
from selenium.webdriver.support.ui import WebDriverWait # 웹페이지가 전부 로드될때까지 기다리는 (Explicitly wait) 기능을 하는 모듈입니다
from webdriver_manager.chrome import ChromeDriverManager # 크롬에서 크롤링을 하기 위해, 웹 드라이버를 설치하는 모듈입니다
from selenium.webdriver.support import expected_conditions as EC # 크롬의 어떤 부분의 상태를 확인하는 모듈입니다
import time # 정해진 시간만큼 기다리게 하기 위한 패키지입니다
driver = webdriver.Chrome(ChromeDriverManager().install()) # 웹 드라이버를 설치하고, 조종할 수 있는 크롬 창을 실행합니다

driver.get("https://map.naver.com/v5/search/서울 성동구 카페")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
    ) # 네이버 지도의 검색창은 "input_search" 라는 클래스 이름으로 설정되어 있습니다
finally:
    pass

driver.switch_to.frame("searchIframe")

fnm = '' # 맨 첫번째 상호 이름입니다. 다음 페이지에서도 똑같은 상호가 나온다면, 다음 페이지가 없다고 인식하고, brk 값이 바뀌면서 반복문이 종료되지요
brk = 1
res = pd.DataFrame() # 결과 파일은 판다스 데이터프레임으로 입력할겁니다
nameframe = '//*[@id="_pcmap_list_scroll_container"]' # 크롤링할 데이터가 있는 영역 중, 빈 공간을 입력해 뒀습니다
timeframe = '//*[@id="app-root"]'
time.sleep(5)

while brk: # 페이지 설정

    driver.find_element(By.XPATH, nameframe) # 이렇게 find_element 함수만 사용해 놓으면 그 영역이 인식되더라고요
    print("found_element")

    for i in range(1,51): # 1~50번째 상호를 순회하도록 했습니다
        nm = ['NA'] # 상호가 저장될 변수
        addr = ['NA'] # 주소가 저장될 변수

        # Name
        driver.find_element(By.XPATH, nameframe)
        nm = driver.find_elements(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{i}]/div[1]/div[2]/a[1]/div/div/span[1]')
        nm += driver.find_elements(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{i}]/div[1]/div/a[1]/div/div/span[1]')

        # Time
        driver.find_element(By.XPATH, timeframe)
        addr = driver.find_elements(By.XPATH, f'//*[@id="app-root"]/div/div/div/div[6]/div/div[2]/div/div/div[3]/div/a/div[2]/div/span/div')
        # print(addr)
        //*[@id="app-root"]/div/div/div/div[6]/div/div[2]/div/div/div[3]/div/a/div[2]/div/span/div
        //*[@id="_pcmap_list_scroll_container"]/ul/li[28]/div[1]/div[1]/a/div/div/span[1]
        //*[@id="_pcmap_list_scroll_container"]/ul/li[28]/div[1]/div[1]/a/div/div
        # addr += driver.find_elements(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{i}]/div[1]/div/div/div/span/a/span[1]')


        if nm != []: # 이름이 비어있으면 아무것도 안하도록 했습니다
            # addr = addr[0].text
            # if any(i in addr for i in ['성동구']): 
            #     res = pd.concat([res, pd.DataFrame([nm[0].text, addr]).T]) # res 데이터프레임에 차곡차곡 쌓아줍니다
            #     res.to_csv('./res/cafe.csv', index=False) # 데이터가 실시간으로 저장되도록 합니다
            res = pd.concat([res, pd.DataFrame([nm[0].text]).T]) # res 데이터프레임에 차곡차곡 쌓아줍니다
            res.to_csv('./source/res/byxhost.csv', index=False) # 데이터가 실시간으로 저장되도록 합니다

        if i == 1: # 첫번째 상호를 불러왔다면, 이전 페이지의 첫번째 상호와 같은지 확인해 줍니다
            if fnm == nm:
                brk = 0
                break

            else:
                fnm = nm


    # 다음 페이지로 넘어가는 코드입니다 다음 버튼을 인식해서 클릭하도록 만들었습니다
    driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div[3]/div[2]')
    driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div[3]/div[2]/a[7]').click()
    time.sleep(2) # 페이지 로딩 시간 2초