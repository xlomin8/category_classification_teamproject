import sys  # 시스템
import os  # 시스템

import pandas as pd  # 판다스 : 데이터분석 라이브러리
import numpy as np  # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup  # html 데이터 전처리
from selenium import webdriver  # 웹 브라우저 자동화
import time  # 시간 지연
import math
import datetime

df_titles = pd.DataFrame()
category = ['bag', 'accessory', 'Jewelry', 'child',
            'w_clothes', 'm_clothes', 'w_shoes',
            'm_shoes', 'clock']

# 크롤링 데이터 수
crawling_no = 15000

# 크롬 웹브라우저 실행
driver = webdriver.Chrome("./chromedriver.exe")

# 사이트 주소
driver.get("https://cafe.naver.com/joonggonara")
time.sleep(2)

# 게시판 클릭
for i in range(2):
    driver.get("https://cafe.naver.com/joonggonara")
    time.sleep(2)
    driver.find_element_by_xpath('// *[ @ id = "menuLink101{}"]'.format(i)).click()

    # // *[ @ id = "menuLink1010] 남성신발
    # // *[ @ id = "menuLink1011] 시곌


# 게시판 프레임 접근
    driver.switch_to.frame("cafe_main")

# 게시글 50개씩 보기
    driver.find_element_by_xpath('//*[@id="listSizeSelectDiv"]').click()    #15씩 보기
    driver.find_element_by_xpath('//*[@id="listSizeSelectDiv"]/ul/li[7]/a').click() #50개씩 보기

# crawling_list = []
    no_app = []
    title_app = []
    nick_app = []
    like_app = []

# 크롤링 해야 할 페이지 계산
    crawling_page = int(math.ceil(crawling_no / 50) + 1)

    try:
        for page in range(1, crawling_page):
            # 페이지 클릭
            driver.find_element_by_link_text(str(page)).click()
            time.sleep(1)
            # 글 번호 수집
            no = [i.text for i in driver.find_elements_by_css_selector('.td_article')]
            no_split = [ni.split()[0] for ni in no]
            # 글 제목 수집
            title = [i.text for i in driver.find_elements_by_css_selector('.article')]
            no_app.append(no_split)
            title_app.append(title)
            # 10페이지 마다 프린트 & 다음 페이지로 클릭
            if str(page)[-1] == '0':
                print(int(page), 'page 크롤링 완료')
                driver.find_element_by_link_text('다음').click()
    # 더이상 페이지가 존재하지 않을 시
    except:
        print('더이상 페이지가 존재하지 않음')
    title_list = sum(title_app, [])
    no_list = sum(no_app, [])
    df=pd.DataFrame({'번호':no_list, '제목':title_list,
                   '분류': category[i]})
    df = df.drop(df[df['번호'] == '필독'].index)
    df = df.drop(df[df['번호'] == '공지'].index)

    df = df.drop(columns=['번호'])
    df = df.reset_index(drop=True)

    df.to_csv('./crawled_data/joonggo_luxury_{}.csv'.format(category[i]), index=False)

driver.close()
