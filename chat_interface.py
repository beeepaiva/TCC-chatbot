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

   
    if prob.item() > 0.65:
        intencao = tag
        
        ###### SE FOR DESCOBRIR SOBRE SALA, HORARIO OU AULAS
        if {key:val for key, val in conversation.items() 
                   if key.startswith("descobrir_")}:
            ##Deve estar presente 
            ## - Semestre e dia
            if "dia" not in entitiesStorage.keys():
                if "dia" in entitiesQuestion.keys():
                    dia = convertDate(entitiesQuestion["dia"])
                    entitiesStorage['dia'] = dia
                else:    
                    dia = date.today()
                    entitiesStorage['dia'] = dia

            if "semestre" not in entitiesStorage.keys():
                if "semestre" in entitiesQuestion.keys():
                    turma = convertNum(entitiesQuestion["semestre"])
                    entitiesStorage['semestre'] = turma
                else:
                    return f"Qual seu semestre?"

            ## PROCURA NO EXCEL
            df = pd.read_excel('./database/database_responses.xlsx')
            values = df[(df['Semestre'] == int(entitiesStorage['semestre'])) & (df['Dia'] == entitiesStorage['dia'].strftime("%Y-%m-%d"))]

            ## DESCOBRIR A INTENÇÃO PRINCIPAL E TRAZER SOMENTE A COLUNA DESEJADA 
            
            if not values.empty:
                i = 0
                j = 0
                Aulas = []
                Hor = []
                Sala = []
                Turmas = []
                TurmaName = []
                while i < len(values.index):
                    while j < len(numpy.unique(values['Turma'])):
                        name = numpy.unique(values['Turma'])[j]
                        TurmaName.append(name[-1:])
                        j+=1
                    Turmas.append(values['Turma'].values[i][-1:])
                    Aulas.append(values['Aula'].values[i])
                    Sala.append(values['Sala'].values[i])
                    Hor.append(values['Horário'].values[i])
                    i += 1

            conversation.clear()
            entitiesStorage.clear()
            lista = []
            ## Se tiver mais de uma turma
            if len(TurmaName) > 1:
                message = ""
                msgTurma = {}
                index = 0 
                while index < len(Aulas):
                    teste = Turmas[index] + " |-| " + Aulas[index] + " |-| " + Sala[index] 
                    if teste not in msgTurma.keys():
                        msgTurma.update({teste:[]})
                        msgTurma[teste].append(Hor[index])
                    else:
                        msgTurma[teste].append(Hor[index])
                    index +=1
                for key in msgTurma:                    
                    HoraInicial = msgTurma[key][0].split("-")[0]
                    HoraFinal = msgTurma[key][len(msgTurma[key])-1].split("-")[1]
                    msgTurma[key] = {"HoraInicio": HoraInicial, "HoraFim": HoraFinal}

                for key in msgTurma:
                    turmam,aula,sala = key.split('|-|')
                    message += f"Turma: {turmam} na sala {sala} tendo a aula {aula.capitalize()} das {msgTurma[key]['HoraInicio']} até {msgTurma[key]['HoraFim']}"        
                    message += '\n'

                return message
            else:
                message = ""
                msgTurma = {}
                index = 0 
                while index < len(Aulas):
                    teste = Turmas[index] + " |-| " + Aulas[index] + " |-| " + Sala[index] 
                    if teste not in msgTurma.keys():
                        msgTurma.update({teste:[]})
                        msgTurma[teste].append(Hor[index])
                    else:
                        msgTurma[teste].append(Hor[index])
                    index +=1
                for key in msgTurma:                    
                    HoraInicial = msgTurma[key][0].split("-")[0]
                    HoraFinal = msgTurma[key][len(msgTurma[key])-1].split("-")[1]
                    msgTurma[key] = {"HoraInicio": HoraInicial, "HoraFim": HoraFinal}

                for key in msgTurma:
                    turmam,aula,sala = key.split('|-|')
                    message += f"\nAula {aula.capitalize()}, na sala {sala} das {msgTurma[key]['HoraInicio']} até {msgTurma[key]['HoraFim']} \n"        
                
                return message
            ## SE NAO FOR BUSCAR CONTEUDO DINAMICO
        else:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    #return f"Mensagem: {random.choice(intent['responses'])}, tag: {intent['tag']}, prob: {prob.item()}"
                    return f"{random.choice(intent['responses'])}"
    else:
        return f"Não entendi, mas você provavelmente pode encontrar essa informação acessando o site! https://www.sp.senac.br/ :)"


def createResponse(aula, sala, turma):
    response = []
    return response