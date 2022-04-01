import numpy as np
import nltk
from nltk.data import load
from nltk.stem.api import StemmerI

from nltk.stem.rslp import RSLPStemmer
stPortugues = RSLPStemmer()      

def tokenizacao(frase):
	return nltk.word_tokenize(frase)

def stem(palavra):
	return  stPortugues(palavra.lower())

def bagOfWords(fraseToken, todasPalavras):
    fraseToken = [stPortugues.stem(w) for w in fraseToken]
    bag = np.zeros(len(todasPalavras), dtype=np.float32)
    for idx, w in enumerate(todasPalavras):
        if w in fraseToken:
            bag[idx] = 1
    return bag