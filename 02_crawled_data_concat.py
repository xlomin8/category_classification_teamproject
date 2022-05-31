import pandas as pd
import glob
import datetime

#경로 불러오기
data_path = glob.glob('./crawled_data/luxury*')
print(data_path)

#csv파일 합치기
df = pd.DataFrame()
for path in data_path[0:]:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])
#혹시 있을지도 모르는 NaN값 제거
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True) #index있는 거 합칠때 drop=True가 필수

# print(df['분류'].value_counts())
# df.info()

# csv파일 저장
df.to_csv('./crawled_data/joonggo_luxury_items_concat_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)