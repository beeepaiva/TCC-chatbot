# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 14:46:52 2022

@author: beeep
"""

import json
import random
from time import strftime
import torch
from model import Neural
from nlp_inicial import bagOfWords, tokenizacao, spacyEntities
from nltk.stem.rslp import RSLPStemmer
import pandas as pd
from datetime import date
from actions import convertNum, convertDate
import numpy


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

   
    if prob.item() > 0.75:
        intencao = tag
        
        ###### SE FOR DESCOBRIR SOBRE SALA, HORARIO OU AULAS
        if {key:val for key, val in conversation.items() 
                   if key.startswith("descobrir_")}:
            ##Deve estar presente 
            ## - Semestre e dia
            if "dia" in entitiesQuestion.keys():
                dia = convertDate(entitiesQuestion["dia"])
            else:    
                dia = date.today()

            if "semestre" in entitiesQuestion.keys():
                turma = convertNum(entitiesQuestion["semestre"])
            else:
                return f"Qual seu semestre?"

            ## PROCURA NO EXCEL
            df = pd.read_excel('./database/database_responses.xlsx')
            values = df[(df['Semestre'] == int(turma)) & (df['Dia'] == dia.strftime("%Y-%m-%d"))]

            ## DESCOBRIR A INTENÇÃO PRINCIPAL E TRAZER SOMENTE A COLUNA DESEJADA 
            if not values.empty:
                i = 0
                arrayResponse = {}
                Aulas = []
                Hor = []
                Sala = []
                TurmaA = []
                TurmaB = []
                while i < len(values.index):
                    if turma == 1:
                        if values['Turma'].values[i][len(values['Turma'].values[i])-1] == 'A':
                            TurmaA.append(i)
                        else:
                            TurmaB.append(i)    
                    Aulas.append(values['Aula'].values[i])
                    Sala.append(values['Sala'].values[i])
                    Hor.append(values['Horário'].values[i])
                    i += 1

            conversation.clear()
            if len(numpy.unique(Aulas)) == 1 and len(numpy.unique(Sala)) == 1:
                HoraInicial = Hor[0].split("-")[0]
                HoraFinal = Hor[3].split("-")[1]
            #return f"Mensagem: {intent['responses']} {arrayResponse['Aula'].lower()}, na sala {arrayResponse['Sala']}, tag: {intent['tag']}, prob: {prob.item()}"
                return f"A sua aula é {Aulas[0].lower()}, na sala {Sala[0]} das {HoraInicial} até {HoraFinal}"
            if len(list(set(Aulas))) >= 1 and turma == 1 and len(numpy.unique(Sala)) >= 1:
                msgTurmaA = ""
                msgTurmaB = ""
                for i in TurmaA:
                    msgTurmaA += " " + Aulas[i].lower() + " " + Sala[i] + " " + Hor[i]
                for i in TurmaB:
                    msgTurmaB += " " + Aulas[i].lower()  + " " +  Sala[i]  + " " +  Hor[i]
                return f" Se você for da turma A: {msgTurmaA} ou Turma B: {msgTurmaB}"
            ## SE NAO FOR BUSCAR CONTEUDO DINAMICO
        else:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    #return f"Mensagem: {random.choice(intent['responses'])}, tag: {intent['tag']}, prob: {prob.item()}"
                    return f"Mensagem: {random.choice(intent['responses'])}"
    else:
        return f"Não entendi, mas você provavelmente pode encontrar essa informação acessando o site! https://www.sp.senac.br/ :)"
