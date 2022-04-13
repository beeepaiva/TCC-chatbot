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

    response = get_response(text)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)