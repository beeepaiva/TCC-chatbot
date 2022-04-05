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

from pathlib import Path
def get_response(msg):
    sentence = tokenizacao(msg)
    doc = nlp(msg)
    
#    for chunk in doc.noun_chunks:
#        print(chunk.root.text)
    for ent in doc.ents:
        print(ent.text, ent.label_)

    if ent.text != None:
        return {"msg": ent.text, "tag": "0", "prob": ""}
    else:
        return {"msg": "Não entendi", "tag": "", "prob": ""}