# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 14:46:52 2022

@author: beeep
"""

import json
import random
from time import strftime
import torch
import numpy
from model import Neural
from nlp_inicial import bagOfWords, tokenizacao, spacyEntities
from nltk.stem.rslp import RSLPStemmer
import pandas as pd
import openpyxl
from word2number import w2n
from datetime import date

stPortugues = RSLPStemmer()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('./database/intents.json', encoding='utf-8') as f:
    intents = json.load(f)
    
FILE = "./database/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = Neural(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Bea"
context = ""
conversation = {}

def get_response(msg):
    sentence = tokenizacao(msg)
    X = bagOfWords(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    entitiesQuestion = {}
    doc = spacyEntities(msg)
    for ent in doc.ents:
        entitiesQuestion.update({ent.label_: ent.text})

    # o que o usuario quer
    # entitiesQuestion[]
    
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    conversation.update({tag: msg})
    
    if prob.item() > 0.75:
        intencao = tag
        ##Deve estar presente 
        ## - Semestre e dia
        if "dia" in entitiesQuestion.keys():
            dia = entitiesQuestion["dia"]
        else:    
            dia = date.today()

        if "semestre" in entitiesQuestion.keys():
            turma = entitiesQuestion["semestre"]
        else:
            return f"Qual seu semestre?"
    
        ## PROCURA NO EXCEL
        wb = openpyxl.load_workbook('./database/database_responses.xlsx')
        ws = wb["Planilha1"]

        list_with_values=[]
        for cell in ws[1]:
            list_with_values.append((cell.value).lower())

        df = pd.read_excel('./database/database_responses.xlsx')
        values = df[(df['Semestre'] == int(turma)) & (df['Dia'] == dia.strftime("%Y-%m-%d"))]
        print(values)

        if not values.empty():
            array_response = []
            for val in values:
                array_response.append(val)

        ## DESCOBRIR A INTENÇÃO PRINCIPAL E TRAZER SOMENTE A COLUNA DESEJADA 

        if prob.item() > 0.75:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                        #Retornando a mensagem, a tag(intencao) e probabilidade da resposta
                    return f"Mensagem: {random.choice(intent['responses'])}, tag: {intent[tag]}, prob: {prob.item()}"
        else:
            return f"Não entendi"
