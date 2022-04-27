from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat_interface import get_response

app = Flask(__name__)
CORS(app)

#function called by the html to get the response from chatbot
@app.post("/predict")
def predict():
    text = request.get_json().get("message")

    response = get_response(text)

    text_file = open("./log.txt", "a")
 
    #write string to file
    text_file.write(f'Entrada: {text}\n')
    text_file.write(f'Saida: {response}\n')

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)