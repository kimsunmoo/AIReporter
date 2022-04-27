import os
import numpy as np
import re
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

from config import UTAGGER_HOME, ARTICLE_PATH, KEYWORD_PATH

CURRENT_DIR = os.getcwd()     # 추후 분석할 파일이 있는 fold 저장
os.chdir(UTAGGER_HOME)       # UTagger가 설치된 fold로 이동

sys.path.append(UTAGGER_HOME)
from utagger_use import *
os.chdir(CURRENT_DIR)

def keyFile():
    keys = get_keyword(2, os.path.join(ARTICLE_PATH, 'article.txt'))

    with open(os.path.join(KEYWORD_PATH, "keys.txt"),"w",encoding="utf-8") as f:
        for key in keys:
            f.write(key + ' ')
            
def get_keyword(num, txt_name):
    nouns=split_nouns(open_txt(txt_name))
    words_graph, idx2word = build_words_graph(nouns)
    word_rank_idx = get_ranks(words_graph)
    sorted_word_rank_idx =  sorted(word_rank_idx, key=lambda k:word_rank_idx[k], reverse= True)
    return keywords(num,idx2word,sorted_word_rank_idx)

def split_nouns(sentences):
    split = []
    
    for line in sentences:
        split.append(extract_pos_tag_line(line))
    
    nouns = []
    vstr = ""
    for a in split :
        for b in a  :     
            vstr = vstr + str(b) + " "
        vstr = vstr.rstrip(" ") 
        vstr = vstr + '\n'
    
    nouns = vstr.split("\n")
    return nouns

def build_words_graph(sentence): #키워드추출
    cnt_vec = CountVectorizer()
    cnt_vec_mat = normalize(cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
    vocab = cnt_vec.vocabulary_
    return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}

def open_txt(name):
    f = open(name,"r",encoding="utf-8")
    sentences = []
    while True:
        line = f.readline()
        if(len(line) == 1):
            continue
        sentences.append(line.strip())
        if(not line):
            break
    f.close
    return sentences

def get_ranks(graph, d = 0.85):
    A = graph
    matrix_size = A.shape[0]
    for id in range(matrix_size):
        A[id, id ] = 0
        link_sum = np.sum(A[:,id])
        if link_sum != 0:
            A[:, id] /=link_sum
        A[:, id] *= -d
        A[id, id] = 1
    B = (1-d) * np.ones((matrix_size,1))
    ranks = np.linalg.solve(A, B)
    return {idx: r[0] for idx, r in enumerate(ranks)}

def keywords(word_num,idx2word,dic):
    keywords = []
    index = []
    for idx in dic[:word_num]:
        index.append(idx)
        
    index.sort()
    for idx in index:
        keywords.append(idx2word[idx])
    return keywords

def extract_pos_tag_line(result, type=0):
    POS_TAG = {'NNG', 'NNP'}  
#     if (type == 0):
#         POS_TAG = {'NNG', 'NNP'}     # 형태소분석 후 추출할 TAG SET
#     elif (type == 1):
#         POS_TAG = {'VA', 'VV', 'VCN'}
#     else:            # 다른 품사(MAG, MAJ, MM 등)
#         POS_TAG = {'MAG', 'MAJ', 'MM', 'XPN', 'XSN'}

    sentence = ut.tag_line(result, 3) 
    words_list = []
    
    sentence = re.sub(r'__\d{2,6}','',sentence) # 동형이의어 번호 제거
    tagged_ej = sentence.split()   # 이런__01/MM 스케일__01/NNG+을/JKO 일제__02/NNG+는/JX ...

    for eojel in tagged_ej:
        morphs = eojel.split('+')    # 형태소 단위로 분리
        for morph in morphs:
            root_tag = morph.split('/')    # 어근 TAG 분리
            if (root_tag[1] in POS_TAG):
                if (type == 1):
                    words_list.append(root_tag[0]+'다')
                else:
                    words_list.append(root_tag[0])
                
    return( words_list )