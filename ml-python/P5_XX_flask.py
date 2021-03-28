from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict/<string:str_predict>')
def predict(str_predict):
    return str_predict