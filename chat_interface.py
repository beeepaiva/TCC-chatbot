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
import string
import os
import unidecode


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

conversation = {}
entitiesStorage = {}

def get_response(msg):
    sentence = tokenizacao(unidecode.unidecode(msg))
    X = bagOfWords(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    # dict para identificar entidade e seu valor na mensagem
    entitiesQuestion = {}
    doc = spacyEntities(unidecode.unidecode(msg))
    for ent in doc.ents:
        entitiesQuestion.update({ent.label_: ent.text})

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    conversation.update({tag: msg})
   
   ## Se tiver mais de 65% de chance de ser a intenção, ele responde
    if prob.item() > 0.65:
        
        ###### SE FOR DESCOBRIR SOBRE SALA, HORARIO OU AULAS
        if {key:val for key, val in conversation.items() 
                   if key.startswith("descobrir_")}:
            ##Deve estar presente 
            ## - Semestre e dia
            # Caso o dia não esteja presente, automaticamente pega o HOJE 
            # Se o semestre não estiver presente, ele pergunta 
            if "dia" not in entitiesStorage.keys():
                if "dia" in entitiesQuestion.keys():
                    dia = convertDate(entitiesQuestion["dia"].lower())
                    entitiesStorage['dia'] = dia
                else:    
                    dia = date.today()
                    entitiesStorage['dia'] = dia

            if "semestre" not in entitiesStorage.keys():
                if "semestre" in entitiesQuestion.keys():
                    turma = convertNum(entitiesQuestion["semestre"].lower())
                    entitiesStorage['semestre'] = turma
                else:
                    return f"Qual seu semestre?"

            ## PROCURA NO EXCEL
            df = pd.read_excel('./database/database_responses.xlsx')
            values = df[(df['Semestre'] == int(entitiesStorage['semestre'])) & (df['Dia'] == entitiesStorage['dia'].strftime("%Y-%m-%d"))]
            
            if not values.empty:
                i, j = 0,0
                # Arrays para salvar as aulas, salas, turmas e horarios que retornaram da pesquisa
                Aulas, Horarios, Salas, Turmas = ([] for i in range(4))
                # Para mais de uma turma 
                TurmaID = []
                while i < len(values.index):
                    while j < len(numpy.unique(values['Turma'])):
                        idTurma = numpy.unique(values['Turma'])[j]
                        TurmaID.append(idTurma[-1:])
                        j+=1
                    Turmas.append(values['Turma'].values[i][-1:])
                    Aulas.append(values['Aula'].values[i])
                    Salas.append(values['Sala'].values[i])
                    Horarios.append(values['Horário'].values[i])
                    i += 1
            else:
                del entitiesQuestion['semestre']
                del entitiesStorage['semestre']
                return f"Nada foi encontrado :("

            #Limpa o contexto que salva as entidades da conversa e a conversa
            conversation.clear()
            entitiesStorage.clear()

            ## Gerando resposta conforme quantidade de turmas
            # id enviado corresponde ao tipo de mensagem que será criada 
            # 1 - mais de uma turma e 0 - uma turma
            if len(TurmaID) > 1:
                message = createResponse(Aulas, Salas, Turmas, Horarios, 1)
                return message
            else:
                message = createResponse(Aulas, Salas, Turmas, Horarios, 0)
                return message
        ## SE NAO FOR BUSCAR CONTEUDO DINAMICO
        else:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    return f"{random.choice(intent['responses'])}"
    else:
        return f"Não entendi, mas você provavelmente pode encontrar essa informação acessando o site! https://www.sp.senac.br/ :)"


#Função que cria a mensagem de resposta. 
# Recebe os Arrays, e o id para devolver com ou sem a turma
def createResponse(aulasResponse, salasResponse, turmasResponse, horariosResponse, id):
    message = ""
    msgTurma = {}
    z = 0 
    while z < len(aulasResponse):
        keyReponse = turmasResponse[z] + " |-| " + aulasResponse[z] + " |-| " + salasResponse[z] 
        if keyReponse not in msgTurma.keys():
            msgTurma.update({keyReponse:[]})
            msgTurma[keyReponse].append(horariosResponse[z])
        else:
            msgTurma[keyReponse].append(horariosResponse[z])
        z +=1
        
    for key in msgTurma:                    
        HoraInicial = msgTurma[key][0].split("-")[0]
        HoraFinal = msgTurma[key][len(msgTurma[key])-1].split("-")[1]
        msgTurma[key] = {"HoraInicio": HoraInicial, "HoraFim": HoraFinal}

    for key in msgTurma:
        turmaN,aula,sala = key.split('|-|')
        if id == 1:
            message += f' - Turma {turmaN} na sala {sala} tendo a aula {string.capwords(aula)} das {msgTurma[key]["HoraInicio"]} até {msgTurma[key]["HoraFim"]}<br>'
        else:
            message += f' - Aula {string.capwords(aula)}, na sala {sala} das {msgTurma[key]["HoraInicio"]} até {msgTurma[key]["HoraFim"]}<br>'
    
    return message