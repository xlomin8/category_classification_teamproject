# <저장해놓은 데이터 크롤링 코드 + 데이터 전처리 코드 + 모델 => 예측>
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)    #20column까지는 모두 출력
df = pd.read_csv('./crawling_data/naver_headline_news_20220527.csv')
# print(df.head())
# df.info()

#라벨링
X = df['제목']  #입력
Y = df['분류']  #타겟 9개

#저장해놓은 pickled encoder 불러오기
with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

labeled_Y = encoder.transform(Y)
label = encoder.classes_


#onehot encoding (가변수화)
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)

#X 전처리
okt = Okt() #openkoreantokenizer: 피팅 후 딕셔너리 형태
# okt_morph_X = okt.morphs(X[7], stem=True)  #morphs: 형태소 단위로 잘라주는 함수 / stem=True: 어근으로 변환해줌
# print(okt_morph_X)  #형태소 리스트

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
# print(X[:10])

#불용어 dataframe 만들기
stopwords = pd.read_csv('crawling_data/stopwords.csv', index_col=0)   #0번 column이 인덱스다!
# print(stopwords.head())

#불용어 제거하고 남은 형태소 리스트 만들기
# X 속 모든 리스트 요소
for i in range(len(X)):
    words = []
    # X 속 모든 리스트 요소의 j번째 요소
    for j in range(len(X[i])):
        # 한 글자 이상인 형태소만 추출
        if len(X[i][j]) > 1:
            # 불용어 제거
            if X[i][j] not in list(stopwords['stopword']):
                words.append(X[i][j])
    X[i] = ' '.join(words)

#저장해놓은 token 불러오기
with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])

#tokened_X 속 max값을 가진 요소 찾기
for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 17:
        tokened_X[i] = tokened_X[i][:17]

#padding
X_pad = pad_sequences(tokened_X, 17)
print((X_pad[:5]))

#모델 불러오기
model = load_model('./models/news_category_classification_model_0.7087541818618774.h5')
preds = model.predict(X_pad)

#예측 max값의 column 리스트 만들기
predicts = []
for pred in preds:
    most = label[np.argmax(pred)]   #확률 max값의 label
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)] #두번째로 큰 확률의 label
    predicts.append([most, second])
df['predict'] = predicts

print(df.head(30))


#예측 적중 여부 확인
df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 'O'
    else:
        df.loc[i, 'OX'] = 'X'
print(df.head(30))


#정답률 확인
print(df['OX'].value_counts())  #정답수
print(df['OX'].value_counts()/len(df))  #정답률

#예측 실패 출력
for i in range(len(df)):
    if df['category'][i] not in df['predict'][i]:
        print(df.iloc[i])



#예측 적중률을 높이려면?
# 1. 많은 데이터 수집
# 2. 카테고리를 확실하게 분류하기 어려운 데이터들에 핸디캡 부여