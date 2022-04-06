from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat_interface import get_response

app = Flask(__name__)
CORS(app)
#renderizacao do html
#@app.get("/")
#def index_get():
#    return render_template("./index.html")

#prediction
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    #pega do chat que já foi treinado com os dados
    getResponse = get_response(text)
    #if getResponse != "Não entendi o que disse":
    response = getResponse["msg"]
    prob = getResponse["prob"]
    tag = getResponse["tag"]
    message = {"resposta": response, "prob": prob, "tag": tag}
    return jsonify(message)
    #else:
    #    return getResponse

if __name__ == "__main__":
    app.run(debug=True)