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
from word2numberi18n import w2n
from datetime import date, timedelta
from text_to_num import text2num
from text_to_num import alpha2digit
from text_to_num.lang.portuguese import OrdinalsMerger

omg = OrdinalsMerger()
USE_PT_ORDINALS_MERGER = True

stPortugues = RSLPStemmer()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('./database/intents.json', encoding='utf-8') as f:
    intents = json.load(f)
    
instance = w2n.W2N(lang_param="pt")  
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
entitiesStorage = {}

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

    ###### SE FOR DESCOBRIR SOBRE SALA, HORARIO OU AULAS
    if prob.item() > 0.75:
        intencao = tag
        ##Deve estar presente 
        ## - Semestre e dia
        #if "dia" not in entitiesStorage.keys():
        if "dia" in entitiesQuestion.keys():
            ### Tratativa de datas (Tem outra forma????)
            if entitiesQuestion["dia"] == "amanhã":
                dia = date.today()+ timedelta(days=1)
            if entitiesQuestion["dia"] == "hoje":
                dia = date.today()
                #dia = entitiesQuestion["dia"]
        else:    
            dia = date.today()

    #    entitiesStorage.update({'dia': dia})

        #if "semestre" not in entitiesStorage.keys():
        if "semestre" in entitiesQuestion.keys():
            turma = entitiesQuestion["semestre"]
        else:
            return f"Digite o número do seu semestre?"

        #entitiesStorage.update({'semestre': turma})
        ## PROCURA NO EXCEL

        df = pd.read_excel('./database/database_responses.xlsx')
        values = df[(df['Semestre'] == int(turma)) & (df['Dia'] == dia.strftime("%Y-%m-%d"))]
        print(values)

        ## DESCOBRIR A INTENÇÃO PRINCIPAL E TRAZER SOMENTE A COLUNA DESEJADA 
        if not values.empty:
            i = 0
            arrayResponse = {}
            array_responseAula = {}
            array_responseSala = {}
            array_responseHorario = {}
            while i < len(values.index):
                arrayResponse.update({
                    "Aula": values['Aula'].values[i],
                    "Sala": values['Sala'].values[i],
                    "Horario":""
                })
                i += 1
        

        if prob.item() > 0.75:
            for intent in intents["intents"]:
                if next(iter(conversation)) == intent["tag"]:
                        #Retornando a mensagem, a tag(intencao) e probabilidade da resposta
                    conversation.clear()
                    return f"Mensagem: {intent['responses']} {arrayResponse['Aula'].lower()}, na sala {arrayResponse['Sala']}, tag: {intent['tag']}, prob: {prob.item()}"
        else:
            return f"Não entendi"
