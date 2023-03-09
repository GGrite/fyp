from flask import Flask, request, render_template
# from flask import Response, jsonify
# import json
from sqlalchemy import create_engine
from pandas import DataFrame

from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import text_similarity
import lstm_predict
# from bert_classifier import BERTClassifier
# import bert_classifier

import time
start = time.time()

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/guilty', methods=['GET'])
def is_guilty():
    input_txt = request.args.get('inputtext')
    
    guilty = lstm_predict.sentiment_predict(input_txt)
    # result = classifier.is_guilty(input_txt)

    sim_result = text_similarity.similar_case([input_txt] , X, vectorizer, num_insult)
    best_i = sim_result[0]
    similar_list = sim_result[1]
    similar_list.sort(key=lambda x: x[0]) 

    cases = []
    for distance,index in similar_list[:10]:
        cases.append({"title":insult_titles[index], "whole_txt":whole_txt[index]})
    if len(similar_list) == 0:
        cases.append({"title":insult_titles[best_i], "whole_txt":whole_txt[best_i]})

    return render_template('result.html', guilty=guilty, cases=cases, text=input_txt)   # jsonify({"guilty" : result})



@app.route('/similar')
def similar_cases():
    input_txt = [request.args.get('inputtext')] 
    result = text_similarity.similar_case(input_txt, X, vectorizer, num_insult)
    best_i = result[0]
    similar_list = result[1]
    similar_list.sort(key=lambda x: x[0]) 

    cases = []
    for distance,index in similar_list[:10]:
        cases.append({"title":insult_titles[index], "whole_txt":whole_txt[index]})
    if len(similar_list) == 0:
        cases.append({"title":insult_titles[best_i], "whole_txt":whole_txt[best_i]})

    return render_template('similar.html',cases=cases )


@app.route('/case', methods=['GET'])
def case_detail():
    title = request.args.get('title') # request.form['title']
    query = app.database.execute("SELECT insult, whole_txt FROM cases where title ='" + str(title) + "'")
    Data = DataFrame(query.fetchall())
    Data = Data.iloc[0]

    insult_txt, whole_txt  = Data['insult'], Data['whole_txt']
    whole_txt = whole_txt.split('\n')

    return render_template('case.html', title=title ,whole_txt=whole_txt, insult_txt=insult_txt ) # Response(json.dumps(result), mimetype='application/json')


#### DB setting
database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
app.database = database
query = app.database.execute("SELECT title, insult, whole_txt FROM cases")
Data = DataFrame(query.fetchall())
insult_titles, insult_texts, whole_txt  = Data['title'], Data['insult'], Data['whole_txt']

#### text-similarity initialization
okt = Okt()
tokens_all = [okt.morphs(row) for row in insult_texts]

insult_vec = []
for tokens in tokens_all : # tokens_noun:
    text = ''
    for word in tokens:
        text = text + ' ' + word
    insult_vec.append(text)

vectorizer = TfidfVectorizer(min_df = 1, decode_error='ignore')
X = vectorizer.fit_transform(insult_vec)
X.toarray().transpose()
num_insult, num_features = X.shape

print("finish vectorizing all cases : ", start-time.time())


if __name__ == '__main__': # compile
    app.run()