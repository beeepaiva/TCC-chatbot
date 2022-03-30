import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("pt")

import json

with open('intents.json', 'r') as f:
	intents = json.load(f)

training_data = []
#training_data = [
#  ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
#]

for intent in intents['intents']:
	tag = intent['tag']
	for pattern in intent['patterns']:
		training_data.append((pattern, [(0, len(pattern), tag)]))



# the DocBin will store the example documents
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./train.spacy")