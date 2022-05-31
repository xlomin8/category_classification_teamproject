import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

X_train, X_test, Y_train, Y_test = np.load('./crawled_data/joonggo_data_max_30_wordsize_16350.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

#모델 만들기
model = Sequential()
#단어 개수(16350)만큼의 차원 공간에 벡터라이징(차원만 증가시키면 데이터는 희소해짐) -> 300차원으로 줄이기
model.add(Embedding(16350, 300, input_length=30))
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu')) #문장은 하나의 차원 속에 선후관계가 있으므로 Conv1D 사용
model.add(MaxPooling1D(pool_size=1))    #poolingX => 원본 그대로
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(9, activation='softmax'))

model.summary()


#모델 학습
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs=5, validation_data=(X_test, Y_test))

#모델 저장
# model.save('./models/joonggo_category_classification_model_{}_kkma.h5'.format(fit_hist.history['val_accuracy'][-1]))

#plot 그리기
plt.plot(fit_hist.history['loss'], 'b-', label='train loss')
plt.plot(fit_hist.history['val_loss'], 'r--', label='train val_loss')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend()
plt.show()

plt.plot(fit_hist.history['accuracy'], 'b-', label='train accuracy')
plt.plot(fit_hist.history['val_accuracy'], 'r--',  label='val_accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend()
plt.show()
