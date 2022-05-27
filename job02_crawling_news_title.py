# <드라이버 활용해 기사 제목 크롤링>
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics','Economic','Social','Culture','World','IT']
#섹션 별 기사 갯수를 '세계'면으로 맞추기
pages = [110, 110, 110, 78, 110, 66] # IT, 생활로 맞추면 데이터 손실이 너무 커짐

# 크롬 설정 - 크롬 정보 - 버전 확인 - 버전에 맞는 chromedriver 다운로드 - 프로젝트 폴더에 chromedriver 실행파일 복사

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=2'

#webdriver crawling을 위한 각종 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')  #브라우저 창 띄우기 않기
options.add_argument('lang=ko_KR') #언어설정
# options.add_argument('--no-sandbox') # Docker
# options.add_argument('--disable-dev-shm-usage') #리눅스
# options.add_argument('--disable-gpu') #리눅스 - 셀레니움의 작업 속도를 높이기 위해 gpu 기능 제거

#크롬 브라우저를 실행하는 드라이버 만들기
driver = webdriver.Chrome('./chromedriver', options=options)

#브라우저에서 crawling
df_titles = pd.DataFrame()
#모든 카테고리
for i in range(0,6):
    titles = []
    # 모든 페이지
    for j in range(1,pages[i]+1):
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i,j)
        driver.get(url)
        time.sleep(0.2) #페이지 당 0.2초동안 잠깐 멈추기(페이지 로딩 시간을 고려)
        for k in range(1,5):
            for l in range(1,6):
                # 기사 헤드라인의 X-path 규칙 확인 후 X-path를 기준으로 crawling
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k,l)
                try:
                    title = driver.find_element_by_xpath(x_path).text
                    title = re.compile('[^가-힣 ]').sub('', title)
                    titles.append(title)
                except NoSuchElementException as e: #X-path가 없음
                    time.sleep(0.5)
                    try:
                        title = driver.find_element_by_xpath(x_path).text
                        title = re.compile('[^가-힣 ]').sub('', title)
                        titles.append(title)
                    except:
                        try:
                            x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k,l)
                            title = re.compile('[^가-힣 ]').sub('', title)
                            titles.append(title)
                        except:
                            print('no such element')
                except StaleElementReferenceException as e: #페이지가 완전히 로딩되기 전에 X-path를 참조하는 경우
                    print(e)
                    print(category[i], j, 'page', k * l)
                except :
                    print('error')
        #30페이지씩 crawling 할 때마다 임시로 저장
        if j % 30 == 0 :
            df_selection_titles = pd.DataFrame(titles, columns=['titles'])
            df_selection_titles['category'] = category[i]
            df_titles = pd.concat([df_titles, df_selection_titles], ignore_index=True)
            df_titles.to_csv('./crawling_data_{}_{}_{}.csv'.format(category[i], j-29, j), index=False)
            title = [] #30개씩 저장하고 title을 비워둠
    #30페이지씩 crawling 하고 남은 페이지 저장
    df_selection_titles = pd.DataFrame(titles, columns=['titles'])
    df_selection_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_selection_titles], ignore_index=True)
    df_titles.to_csv('./crawling_data_{}_last.csv'.format(category[i]), index=False)
    titles=[]
#최종 합본 (누적O)
df_section_titles = pd.DataFrame(titles, columns=['titles'])
df_section_titles['category'] = category[i]
df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
#csv 파일로 저장
df_titles.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
driver.close()



#1페이지의 헤드라인 밑 20개의 기사들 x-path (5개씩 묶임)
# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a    1
# //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a    2
# //*[@id="section_body"]/ul[1]/li[3]/dl/dt[2]/a    3
# //*[@id="section_body"]/ul[1]/li[4]/dl/dt[2]/a    4
# //*[@id="section_body"]/ul[1]/li[5]/dl/dt[2]/a    5
# ----------------------------------------------
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a    6
# //*[@id="section_body"]/ul[2]/li[2]/dl/dt[2]/a    7
# ----------------------------------------------
# //*[@id="section_body"]/ul[3]/li[1]/dl/dt[2]/a    11
# ----------------------------------------------
# //*[@id="section_body"]/ul[4]/li[5]/dl/dt[2]/a    20