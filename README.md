
# Trabalho de conclusão de curso - Bacharelado em Ciência da Computação
## Chatbot

Foi desenvolvido um bot inteligente para que alunos do curso consigam tirar dúvidas sobre o Senac ou sobre seu curso
de forma rápida e prática.



## Temas abordados

- Treinamento por redes Neurais
- Treinamento e identificação de Entidades e Intenções 
- Busca em excel para trazer dados em forma de respostas dinâmicas
- Criação de uma aplicação Web


## Instalação

1 - Clone do projeto 
```bash
    git clone https://github.com/beeepaiva/TCC-chatbot.git
```

2 - Criação e ativação do ambiente virtual em Python
```bash
  python -m venv venv
  .\venv\Scripts\activate.ps1
```
    
3 - Para treinar a rede neural com base no intents.json
```bash
  python train.py
```

4 - Para treinar a identificação de entidades com o spaCy
```bash
  python preprocess.py
  python -m spacy train config.cfg --outpu ./output --paths.train ./corpus/train.spacy --paths.dev ./corpus/dev.spacy
```

5 - Rodar o serviço do Flask
```bash
  python app.py
```

6 - Por enquanto, o projeto rodando StandAlone, após rodar o serviço do Flask basta apenas abrir o index.html
## Autores

- [@beeepaiva](https://www.github.com/beeepaiva)

