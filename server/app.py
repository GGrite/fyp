from flask import Flask, request
from flask import Response, jsonify
import json
from sqlalchemy import create_engine

from pandas import DataFrame
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import text_similarity
import classifier
from classifier import BERTClassifier

import time
start = time.time()

app = Flask(__name__)
app.config.from_pyfile("config.py")

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

print("finish vectorizing all case data : ", start-time.time())


@app.route('/guilty', methods=['GET'])
def is_guilty_():
    input_txt = request.form['text']  # text form
    result = classifier.is_guilty(input_txt)

    return jsonify({"guilty" : result})
    

@app.route('/case', methods=['GET'])
def similar_cases():
    input_txt = [request.form['text']]  # text form
    result = text_similarity.similar_case(input_txt, X, vectorizer, num_insult)
    best_i = result[0]
    similar_list = result[1]

    print()
    # print("Best index = %i, Best dist = %.2f" % (best_i, best_dist))
    print(input_txt)
    print(insult_texts[best_i])
    print("end------")

    similar_list.sort(key=lambda x: x[0]) 
    print(similar_list)
    result = []
    for distance,index in similar_list[:10]:
        result.append({"title":insult_titles[index], "whole_txt":whole_txt[index]})
    if len(similar_list) == 0:
        result.append({"title":insult_titles[best_i], "whole_txt":whole_txt[best_i]})

    return Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__': # compile
    app.run()