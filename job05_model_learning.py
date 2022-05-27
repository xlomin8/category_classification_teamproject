# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"   #CPU를 쓰도록 강제

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

X_train, X_test, Y_train, Y_test = np.load('crawling_data/news_data_max_17_wordsize_12426.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

#모델 만들기
model = Sequential()
#단어 개수(12426)만큼의 차원 공간에 벡터라이징(차원만 증가시키면 데이터는 희소해짐) -> 300차원으로 줄이기
model.add(Embedding(12426, 300, input_length=17))
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu')) #문장은 하나의 차원 속에 선후관계가 있으므로 Conv1D 사용
model.add(MaxPooling1D(pool_size=1))    #poolingX => 원본 그대로
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='softmax'))

model.summary()


#모델 학습
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs=10, validation_data=(X_test, Y_test))

#모델 저장
model.save('./models/news_category_classification_model_{}.h5'.format(fit_hist.history['val_accuracy'][-1]))

plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()
