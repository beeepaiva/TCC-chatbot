import srsly
import typer
import warnings
from pathlib import Path

import spacy
from spacy.tokens import DocBin

nlp = spacy.load("pt_core_news_lg")
TRAIN_DATA = [
  ("Qual a matéria de hoje?", [(7, 13, "MATERIA")]),
  ("Qual a aula de hoje?", [(7, 10, "MATERIA")]),
  ("Hoje eu tenho qual matéria?", [(20, 27, "MATERIA")]),
  ("Quais matérias de hoje?", [(7, 23, "MATERIA_HOJE")]),
  ("Quais aulas de hoje?", [(7, 20, "MATERIA_HOJE")]),
  ("Qual horário de aula?", [(6, 13, "HORARIO")]),
  ("Que horas começa a aula?", [(5, 9, "HORARIO")]),
  ("Até que horas vai a aula?", [(0, 3, "HORARIO")]),
  ("Em qual sala eu tenho aula?", [(8, 11, "SALA")]),
  ("Qual a sala de hoje?", [(8, 12, "SALA")]),
  ("Onde fica minha sala?", [(16, 20, "SALA")]),
]

def convert(lang: str, input_path: Path, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in srsly.read_json(input_path):
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