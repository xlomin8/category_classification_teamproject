# <url을 통해 네이버 기사 헤드라인 크롤링하기>
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

category = ['Politics','Economic','Social','Culture','World','IT']
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100 #정치
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101 #경제
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102 #사회
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103 #문화
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104 #세계
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105 #IT

#url 통해 크롤링 (웹에서 요청하는 것처럼 위장)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}
            # 개발자 도구 - 네트워크 - 아무 리소스 - 요청 헤더 - user-agent
# resp = requests.get(url, headers=headers)
# soup = BeautifulSoup(resp.text, 'html.parser')
#
# title_tags = soup.select('.cluster_text_headline')


#파싱 시작
df_titles = pd.DataFrame()
for i in range(6):
    # 카테고리 별로 파싱
    url='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    # 주소로 웹페이지 요소 긁어오기
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # re로 전처리
    title_tags = soup.select('.cluster_text_headline')
    titles = []
    for title_tag in title_tags :
        # 자연어 처리(형태소 단위)
        title = re.compile('[^가-힣 ]').sub('', title_tag.text) #한글과 띄어쓰기를 제외한 나머지 모두 제거
        titles.append(title)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

#파싱이 끝난 데이터 -> csv 파일로 저장
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
# df_titles.to_csv('./crawling_data/naver_headline_news{}.csv'.format(datetime.date.today()), index=False)