import numpy as np
import nltk
from nltk.data import load
from nltk.stem.api import StemmerI
import nltk.corpus
from nltk import word_tokenize,pos_tag
from nltk.stem import RSLPStemmer
import spacy

nlp = spacy.load("./output/model-best")

st = RSLPStemmer()        

def tokenizacao(frase):
	return nltk.word_tokenize(frase)

def stem(palavra):
	return  st.stem(palavra.lower())

def lemma(palavra):
    return nltk.WordNetLemmatizer(palavra)


def spacyEntities(msg):
    doc = nlp(msg)
    return doc

def morpho(palavra):
    tokens = word_tokenize(palavra.lower())
    tag=pos_tag(tokens)
    print(tag)

    ne_tree = nltk.ne_chunk(tag)
    print(ne_tree)

def bagOfWords(fraseToken, todasPalavras):
    fraseToken = [stem(w) for w in fraseToken]
    bag = np.zeros(len(todasPalavras), dtype=np.float32)
    for idx, w in enumerate(todasPalavras):
        if w in fraseToken:
            bag[idx] = 1
    return bag