from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from interface import get_response

app = Flask(__name__)
CORS(app)

#prediction
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    #pega do chat que já foi treinado com os dados
    getResponse = get_response(text, show_details=True)
    #if getResponse != "Não entendi o que disse":
    response = getResponse
    message = {"resposta": response['message'], "tag": response['tag'], "prob": response['prob']}
    return jsonify(message)
    #else:
    #    return getResponse

if __name__ == "__main__":
    app.run(debug=True)