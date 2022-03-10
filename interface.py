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


context = {}
ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def get_response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return random.choice(i['responses'])

            results.pop(0)


#carregando o modelo 
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('./model.tflearn')



#print("Em que posso ajudar?")
#print("Para encerrar digite 'sair'")


#while True:
#    entrada = input("Você: ")
#    if entrada == "sair":
#        break
#    response(entrada, show_details=True)
