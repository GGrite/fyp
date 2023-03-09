from konlpy.tag import Okt
import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import pandas as pd
import numpy as np

okt = Okt()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

Data = pd.read_csv('/Users/a/Desktop/final_data.csv')
train_data, test_data = train_test_split(Data, test_size=0.2, random_state=0)

train_data['모욕 문장'] = train_data['모욕 문장'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
train_data['모욕 문장'] = train_data['모욕 문장'].str.replace('^ +', "") # white space 데이터를 empty value로 변경
train_data['모욕 문장'].replace('', np.nan, inplace=True)
train_data = train_data.dropna(how = 'any')
test_data.drop_duplicates(subset = ['모욕 문장'], inplace=True) # 모욕 문장 열에서 중복인 내용이 있다면 중복 제거
test_data['모욕 문장'] = test_data['모욕 문장'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
test_data['모욕 문장'] = test_data['모욕 문장'].str.replace('^ +', "") # 공백은 empty 값으로 변경
test_data['모욕 문장'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
test_data = test_data.dropna(how='any') # Null 값 제거

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
X_train = []
for sentence in tqdm(train_data['모욕 문장']):
    tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
    X_train.append(stopwords_removed_sentence)

X_test = []
for sentence in tqdm(test_data['모욕 문장']):
    tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
    X_test.append(stopwords_removed_sentence)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

max_len = 30
loaded_model = load_model('/Users/a/Desktop/best_model.h5',compile=False)

def sentiment_predict(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    # if(score > 0.5):
    #     print("{:.2f}% 확률로 유죄입니다.\n".format(score * 100))
    #     return ("유죄", round(score*100, 2))
    # else:
    #     print("{:.2f}% 확률로 무죄입니다.\n".format((1 - score) * 100))
    #     return ("무죄", round((1-score)*100,2))
    
    return ("유죄", round(score*100, 2))
