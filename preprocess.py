import srsly
import typer
import warnings
from pathlib import Path
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin

nlp = spacy.load("pt_core_news_lg")

TRAIN_DATA = [
["Onde fica minha sala?",{"entities":[[0,4,"lugar"],[16,20,"sala"]]}],
["Qual a sala de hoje?",{"entities":[[7,11,"sala"],[15,19,"dia"]]}],
["Em qual sala eu tenho aula?",{"entities":[[8,12,"sala"],[22,26,"materia"]]}],
["Até que horas vai a aula?",{"entities":[[0,13,"horario"],[20,24,"materia"]]}],
["Que horas começa a aula?",{"entities":[[4,9,"horario"],[10,16,"horario"],[19,23,"materia"]]}],
["Qual horário de aula?",{"entities":[[5,12,"horario"],[16,20,"materia"]]}],
["Qual a matéria de amanhã?",{"entities":[[7,14,"materia"],[18,24,"dia"]]}],
["Quais aulas de amanhã?",{"entities":[[6,11,"materia"],[15,21,"dia"]]}],
["Quais aulas de hoje?",{"entities":[[6,11,"materia"],[15,19,"dia"]]}],
["Hoje eu tenho qual matéria?",{"entities":[[0,4,"dia"],[19,26,"materia"]]}],
["Qual a aula de hoje?",{"entities":[[7,11,"materia"],[15,19,"dia"]]}],
["Qual a matéria de hoje?",{"entities":[[7,14,"materia"],[18,22,"dia"]]}]

]

def convert():
    lang = "pt"
    input_path = "./intents.json"
    output_path = "./corpus/train.spacy"
    nlp = spacy.blank(lang)
    db = DocBin()

    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)


if __name__ == "__main__":
    typer.run(convert)