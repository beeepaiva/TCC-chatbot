import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Importando lib nltk stem palavras em portugues
from nltk.stem.rslp import RSLPStemmer
stPortugues = RSLPStemmer()
from nltk import tokenize

import pickle
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

#intents.json
import json
# encoding utf-8 pra aceitar acentos
with open('intents.json', encoding='utf-8') as intentsData:
    intents = json.load(intentsData)

#Libs tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

#carregando o modelo 
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


def clean_up_sentence(sentence):
    # tokenize
    sentence_words = tokenize.word_tokenize(sentence, language="portuguese")
    # stem 
    sentence_words = [stPortugues.stem(word.lower()) for word in sentence_words]
    return sentence_words

# procurando nas frases dentro do arquivo p identificar o bag of words
def bow(sentence, words, show_details=False):
    # tokenize 
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

model.load('./model.tflearn')
