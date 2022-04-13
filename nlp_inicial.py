import numpy as np
import nltk
import nltk.corpus
from nltk.stem.rslp import RSLPStemmer
import spacy

stPortugues = RSLPStemmer()

nlp = spacy.load("./output/model-best")

st = RSLPStemmer()        

def tokenizacao(frase):
	return nltk.word_tokenize(frase)

def stem(palavra):
	return stPortugues.stem(palavra.lower())

def lemma(palavra):
    return nltk.WordNetLemmatizer(palavra)

def spacyEntities(msg):
    doc = nlp(msg)
    return doc

def bagOfWords(fraseToken, todasPalavras):
    fraseToken = [stem(w) for w in fraseToken]
    bag = np.zeros(len(todasPalavras), dtype=np.float32)
    for idx, w in enumerate(todasPalavras):
        if w in fraseToken:
            bag[idx] = 1
    return bag