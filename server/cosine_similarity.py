import numpy as np
from konlpy.tag import Okt 
from sklearn.metrics.pairwise import cosine_similarity


def similar_case(input_txt, X, vectorizer, num_insult):
    ### vectorize the input sentence
    okt = Okt()
    input_tokens = [okt.morphs(row) for row in input_txt]

    input_for_vec = []
    for tokens in input_tokens:
        text = ''
        for word in tokens:
            text = text + ' ' + word
            
        input_for_vec.append(text)

    input_vec = vectorizer.transform(input_for_vec)

    ### cosine similarity
    cos_similarities = cosine_similarity(input_vec, X)

    # max_idx = np.argmax(cos_similarities)
    sort_idx = np.argsort(cos_similarities[0])[::-1]

    similar_list = []
    for i in range(5): # top N
        if cos_similarities[0][sort_idx[i]] <= 0.2:
            break
        similar_list.append((cos_similarities[0][sort_idx[i]], sort_idx[i] ))  # similarity, index

    if len(similar_list)==0:
        similar_list.append((cos_similarities[0][sort_idx[0]],sort_idx[0]))

    best_idx = sort_idx[0]

    print(similar_list)

    result = [best_idx, similar_list]
    return result
