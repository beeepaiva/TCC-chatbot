import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Importando lib nltk stem palavras em portugues
from nltk.stem.rslp import RSLPStemmer
stPortugues = RSLPStemmer()
from nltk import tokenize

#Libs tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

# usado pra otimizar a estrutura de dados
import pickle

#intents.json
import json
# encoding utf-8 pra aceitar acentos
with open('intents.json', encoding='utf-8') as intentsData:
    intents = json.load(intentsData)

words = []
tags = []
documents = []
ignore_words = ['.', ';', ',', '!', '?']

#Loop que percorre pelos patterns no intent
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize de palavras usando lib do nltk em portugues
        w = tokenize.word_tokenize(pattern, language="portuguese")
        # adicionando palavra na lista
        words.extend(w)
        documents.append((w, intent['tag']))
        # pegando tags
        if intent['tag'] not in tags:
            tags.append(intent['tag'])

#stem em portugues e lower case
words = [stPortugues.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove tags duplicadas e chamo de classes
classes = sorted(list(set(tags)))

print (len(documents), "documentos")
print (len(classes), "classes", classes)
print (len(words), "palavras já passadas pelo stem", words)

# treino
training = []
output = []

output_empty = [0] * len(classes)

# criando o bag of words
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output '0' pra cada tag e  '1' para tag atual
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

# TESTES
train_x = list(training[:,0])
train_y = list(training[:,1])

# REDE NEURAL com tflearn
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Modelo e tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Inicio do treino
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
#salvando
model.save('model.tflearn')

#usando o pickle
pickle.dump({'words': words, 'classes': classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )
