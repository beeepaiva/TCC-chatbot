import spacy
from spacy.lang.pt import Portuguese

from spacy.matcher import Matcher

import json

nlp = spacy.load("pt_core_news_lg")

with open('intents.json', 'r') as f:
	intents = json.load(f)
#matcher = Matcher(nlp.vocab)
#patterns1 = [
#    [{"TEXT": "aula"}]
#]
#matcher.add("MATERIA", patterns1)

#text = "Eu não precisaria defender o TCC se não o atacassem."
text = "Qual aula tenho hoje?"
tags = []
pat = []

for intent in intents['intents']:
	tag = intent['tag']
	tags.append(tag)
	for pattern in intent['patterns']:
		w = nlp(pattern)
		pat.extend(w)

for pattern in pat:
	for token in pattern.doc:
		for ent in pattern.doc.ents: 
			print(token.text, token.pos_, token.head.text)
			print(ent.text, ent.label_)

#for match_id, start, end in matcher(doc):
#    span = doc[start:end]
#    print("Matched span:", span.text)
#   # Get the span's root token and root head token
#    print("Root token:", span.root.text)
#    print("Root head token:", span.root.head.text)

print("---------------------")
#identificando entidades

   
#text - retorna o texto
#pos_ part-of-speech previsto, tipo da palavra (verbo, adverbio, substantivo...)
#dep_ dependencia
#head sintaxe de onde ele ta ligado
#for token in doc:
#    print(token.text, token.pos_, token.dep_, token.head.text)

#Função de identificação do alfabeto - Pontuação - Numero
#print("is_alpha:", [token.is_alpha for token in doc])
#print("is_punct:", [token.is_punct for token in doc])
#print("like_num:", [token.like_num for token in doc])


