
# 공지 숨기기 클릭
# anno_off = driver.find_element_by_css_selector('.check_box').click()

### Step 0. 준비
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
category = ['m_cos', 'w_e_color', 'perfume']
### Step 1. 크롤링
keyword = "☰ 통합 Q & A ☰"
crawling_no = 40000

# 크롬 웹브라우저 실행
driver = webdriver.Chrome("./chromedriver.exe")

# 사이트 주소
driver.get("https://cafe.naver.com/joonggonara")
time.sleep(2)

# 게시판 클릭
for i in range(0, 3):
    driver.get("https://cafe.naver.com/joonggonara")
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="menuLink37{}"]'.format(i)).click()
    # // *[ @ id = "menuLink370"]
    # // *[ @ id = "menuLink371"]
    # // *[ @ id = "menuLink372"]
# <a href="/ArticleList.nhn?search.clubid=10050146&amp;search.menuid=332&amp;search.boardtype=L" target="cafe_main" onclick="goMenu('332');clickcr(this, 'mnu.sell','','',event);" class="gm-tcol-c" id="menuLink332">
# 						여성 기초화장품
# 					</a>
# 게시판 프레임 접근
    driver.switch_to.frame("cafe_main")

# 게시글 50개씩
    driver.find_element_by_xpath('//*[@id="listSizeSelectDiv"]').click()
    driver.find_element_by_xpath('//*[@id="listSizeSelectDiv"]/ul/li[7]/a').click()

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
            # # 작성자 수집
            # nick = [i.text for i in driver.find_elements_by_css_selector('.p-nick .m-tcol-c')]
            # # 좋아요 수집
            # like = [i.text for i in driver.find_elements_by_css_selector('.td_likes')]
            # 수집 데이터 append
            no_app.append(no_split)
            title_app.append(title)
            # nick_app.append(nick)
            # like_app.append(like)
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
                    # '제목': title_list,
                   '분류': category[i]})
    df = df.drop(df[df['번호'] == '필독'].index)
    df = df.drop(df[df['번호'] == '공지'].index)
    # df = df.drop(df['번호'], axis='columns')
    df = df.drop(columns=['번호'])
    df = df.reset_index(drop=True)
    # df1 = df.sample(frac=0.05)
    df.to_csv('./naver_cosmetic_{}.csv'.format(category[i]), index=False)
    # df1.to_csv('./naver_cosmetic_test.csv'.format(category[i]), index=False)
driver.close()
#
# # 리스트안 리스트 분해
# no_list = sum(no_app, [])
# title_list = sum(title_app, [])
# # nick_list = sum(nick_app, [])
# # like_list = sum(like_app, [])
#
# # 판다스화
# df = pd.DataFrame({'번호': no_list,
#                    '제목': title_list})
#                    # '작성자': nick_list,
#                    # '좋아요': like_list})
# df_section_titles = pd.DataFrame(titles, columns=['titles'])
# df_section_titles['category'] = category[i]  # 위 카테고리 리스트를 인덱싱해서 카테고리별 명으로 분류를함.
# df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)  # concat : 판다스에서 합치는 함수 크롤링 데이터가 누적이됨
# df_titles.to_csv('./crawling_data/naver_news_titles_test{}.csv'.format(
#                     datetime.datetime.now().strftime('%Y%m%d')), index=False, encoding='utf-8-sig')
# # 필독, 공지 삭제
# df = df.drop(df[df['번호'] == '필독'].index)
# df = df.drop(df[df['번호'] == '공지'].index)
# df = df.reset_index(drop=True)
#
# print('글 ', len(df), '개 크롤링 완료. \n크롤링 종료.', sep='')
#
# df.info()
#
# # 저장
# df.to_csv('./naver_cosmetic_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
# # 저작자표시