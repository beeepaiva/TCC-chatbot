import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Libs tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

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
ERROR_THRESHOLD = 0.60
def classify(sentence):
    # a partir do model, gera a probabilidade
    results = model.predict([bow(sentence, words)])[0]
    # filtra as predições
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # ordena pela probabilidade
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # retorna intent e prob
    return return_list

def get_response(sentence, userID="222", show_details=True):
    results = classify(sentence)
    if results:
        while results:
            for i in intents['intents']:
                # encontra a tag
                if i['tag'] == results[0][0]:
                    # setta um contexto se necessario
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # se tiver contexto coloca no historico do usuario
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # retorna resposta aleatoria dentro da identificaçao da tag ou context
                    prob = results[0][1]
                    final_response = {'message': random.choice(i['responses']), 'tag': i['tag'], 'prob': str(prob)}
                    return final_response
            results.pop(0)            
    else:
        return {'message': "Não entendi o que disse", 'tag': "out", 'prob': "0"}


#print("Em que posso ajudar?")
#print("Para encerrar digite 'sair'")

#carregando o modelo 
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('./model.tflearn')


#while True:
#    entrada = input("Você: ")
#    if entrada == "sair":
#        break
#    response(entrada, show_details=True)
