import typer
import spacy
import warnings
from spacy.tokens import DocBin
from spacy.util import minibatch, compounding
from spacy.training import Example

import json

def convert():
    lang = "pt"
    input_path = "./database/entities_training.json"
    output_path = "./corpus/train.spacy"
    nlp = spacy.blank("pt")
    db = DocBin()

    with open(input_path, encoding='utf-8') as f:
        TRAIN_DATA = json.load(f)


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