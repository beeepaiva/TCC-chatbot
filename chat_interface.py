# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 14:46:52 2022

@author: beeep
"""

import json
import random
import torch
import numpy
from model import Neural
from nlp_inicial import bagOfWords, tokenizacao

#Importando lib nltk stem palavras em portugues
from nltk.stem.rslp import RSLPStemmer
stPortugues = RSLPStemmer()

import spacy

nlp = spacy.load("./training/model-best")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)
    
#FILE = "data.pth" data = torch.load(FILE)

#input_size = data["input_size"]
#hidden_size = data["hidden_size"]
#output_size = data["output_size"]
#all_words = data["all_words"]
#tags = data["tags"]
#model_state = data["model_state"]

#model = Neural(input_size, hidden_size, output_size).to(device)
#model.load_state_dict(model_state)
#model.eval()

bot_name = "Bea"


from pathlib import Path
def get_response(msg):
    sentence = tokenizacao(msg)
    doc = nlp(msg)
    
    token = doc[0]
#    for chunk in doc.noun_chunks:
#        print(chunk.root.text)
    for ent in doc.ents:
        print(ent.text, ent.label_)
#    X = bagOfWords(sentence, all_words)
#    X = X.reshape(1, X.shape[0])
#    X = torch.from_numpy(X).to(device)

#    output = model(X)
#    _, predicted = torch.max(output, dim=1)
#    tag = tags[predicted.item()]
    
#    probs = torch.softmax(output, dim=1)
#    prob = probs[0][predicted.item()]
    
#    if prob.item() > 0.75:
#        for intent in intents["intents"]:
#            if tag == intent["tag"]:#Retornando a mensagem, a tag(intencao) e probabilidade da resposta
        if ent.text != None:
            return {"msg": ent.text, "tag": "0", "prob": ""}
        else:
            return {"msg": "Não entendi", "tag": "", "prob": ""}