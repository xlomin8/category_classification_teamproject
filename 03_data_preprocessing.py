# <csv파일 자연어 처리>
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

#concat파일에서 한글, 영어만 남기고 제거하기
df1 = pd.read_csv('./crawled_data/joonggo_luxury_items_concat_20220530.csv')
df1["제목"] = df1["제목"].str.replace(pat=r'[^가-힣a-zA-Z ]', repl=r'', regex=True)
print(df1)
print(df1.info())
print(type(df1))
df1.to_csv("./joonggo_concat_clear.csv", index=False)

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./joonggo_concat_clear.csv')
# print(df.head())
# df.info()

#라벨링
X = df['제목']  #입력
Y = df['분류']  #타겟 9개

encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
# print(labeled_Y[:3])    #[3 3 3]
label = encoder.classes_
# print(label)    #['Culture', 'Economic', 'IT', 'Politics', 'Social', 'World']

#encoder 저장
with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

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
stopwords = pd.read_csv('./crawled_data/stopwords.csv', index_col=0)   #0번 column이 인덱스다!
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
# print(X[1]) #['권성동', '윤종원', '함께', '활동', '하다', '분', '들', '이', '반대', '의견', '제시', '하고', '있다']
# print(X[:5])

#형태소를 숫자로 바꾸기 -> token
token = Tokenizer()
token.fit_on_texts(X)   #fit_on_texts: 유니크한 단어 딕셔너리
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1    #딕셔너리 속 요소의 개수 + 1(0포함)
# print(tokened_X)    #유니크한 단어들 순서대로 라벨링(padding을 위해 0은 안씀)
# print(token.word_index) #문장에 등장하는 순서대로 유니크한 값을 라벨링한 딕셔너리

#tokenizer 저장
with open('./models/news_token.pickle', 'wb') as f:
    pickle.dump(token, f)

#tokened_X 속 max값을 가진 요소 찾기
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

#max값을 기준으로 padding(비어있는 값 0으로 채우기)
X_pad = pad_sequences(tokened_X, max)
print(X_pad)

#holdout
X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

#저장
xy = X_train, X_test, Y_train, Y_test
np.save('./crawled_data/joonggo_data_max_{}_wordsize_{}'.format(max, wordsize), xy)

