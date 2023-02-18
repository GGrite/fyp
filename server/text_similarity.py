from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy as sp

def get_dist(v1, v2): # Euclidean 
    delta = v1 - v2
    return sp.linalg.norm(delta.toarray())


def similar_case(input_txt, X, vectorizer, num_insult):
    okt = Okt()
    input_tokens = [okt.morphs(row) for row in input_txt] # morphs(row) nouns

    input_for_vec = []
    for tokens in input_tokens:
        text = ''
        for word in tokens:
            text = text + ' ' + word
            
        input_for_vec.append(text)

    # transform 
    input_vec = vectorizer.transform(input_for_vec)
    input_vec.toarray()

    best_dist = 65535
    best_i = None

    similar_list = []

    for i in range(0, num_insult):
        post_vec = X.getrow(i)
        d = get_dist(post_vec, input_vec)
        
        # print('== Post %i with dist=%.2f : %s' %(i,d,insult_texts[i]))
        if d < best_dist: 
            best_dist = d
            best_i = i
        
        if d < 1:
            similar_list.append((d,i))

    result = [best_i, similar_list]
            
    return result
