import pandas as pd
import glob
import datetime

#경로 불러오기
data_path = glob.glob('./crawling_data/*')
print(data_path)

#csv파일 합치기
df = pd.DataFrame()
for path in data_path[1:]:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])
#혹시 있을지도 모르는 NaN값 제거
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True) #index있는 거 합칠때 drop=True가 필수

print(df.head())
print(df.tail())
print(df['category'].value_counts())
df.info()
df.to_csv('./crawling_data/naver_news_titles_concat{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
# df.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(datetime.date.today()), index=False)



#에러 없었을 때
# df = pd.read_csv('./crawling_data/crawling_data.csv')
# df_headline = pd.read_csv('./crawling_data/naver_headline_news_220525.csv')
# df_all = pd.concat([df, df_headline], ignore_index=True)
#
# print(df_all.head())
# print(df_all.tail())
# print(df_all['category'].value_counts())
# df_all.info()
# df_all.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
