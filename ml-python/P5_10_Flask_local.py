from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from joblib import dump, load

import numpy as np
import tensorflow as tf

import re
from bs4 import BeautifulSoup
from nltk import download as nltk_download
from nltk import tokenize, RegexpTokenizer, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
nltk_download('wordnet') 
nltk_download('punkt')
nltk_download('stopwords')
nltk_download('averaged_perceptron_tagger')

nltk_stop_words = set(stopwords.words('english') + 
		['use', 'try', 'way', 'want', 'would', 'need', 'one', '1', '2' ] +
		['something', 'desire', 'follow ', 'help', 'please', 'however', 'follow', 'code' ])
wn = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

model_path = "..\\data\\stackoverflow\\models\\"


vector_model = tf.keras.models.load_model(model_path + "LSTM_model")
#vector_model.compile()
#vector_model.load_weights(model_path + "LSTM_weights")

mlb = load(model_path + "LSTM_model\\mlb.joblib")

print("TF VERSION: ", tf.__version__)


title_models = load(model_path + 'title_RidgeClassifier.joblib')
body_models = load(model_path + 'body_RidgeClassifier.joblib')
title_vectorizer = load(model_path + 'lemma_title_vectorizer.joblib')
body_vectorizer = load(model_path + 'lemma_body_vectorizer_12.joblib')


ret = {
	"tags": [
		"tag1",
		"tag2",
		"tag3"
	]
}

app = Flask(__name__)
# CORS(app)
@app.route('/flask/predict/', methods=['POST'])
def predict():
	data = request.json
	if data['model'] == "baseline":
		ret = baseline(data)
		return jsonify(ret)

	if data['model'] == "vector":
		ret = vectorizer(data)
		return jsonify(ret)

	ret = {'Error': "Model not found"}
	return jsonify(ret)

@app.route('/flask/models/', methods=['GET'])
def get_models():
	return jsonify({
		'title': [(k,title_models[k].alpha) for k in title_models.keys()],
		'body': [(k,body_models[k].alpha) for k in body_models.keys()],
	})

if __name__ == '__main__':
    app.run(debug=True)

def bodytobs4(raw_text):
	soup = BeautifulSoup(raw_text, 'html.parser')
	code = ""
	for s in soup.find_all('code'):
		code = code + s.get_text()
		s.extract()
	return re.sub(r'\n+', ' ', soup.get_text()).strip()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatizer(title, body):
	title_tokens = [ lemma for lemma in 
            [ wn.lemmatize(w, get_wordnet_pos(w)) for w in tokenizer.tokenize(title.lower()) ]
            if lemma not in nltk_stop_words ]
	body_tokens = [ lemma for lemma in 
            [ wn.lemmatize(w, get_wordnet_pos(w)) for w in tokenizer.tokenize(bodytobs4(body).lower()) ]
            if lemma not in nltk_stop_words ]
	return title_tokens, body_tokens

def vectorizer(data):
	title_lemmas, body_lemmas = lemmatizer(data['title'], data['body'])
	title_lemmas = [' '.join(title_lemmas)]
	body_lemmas = [' '.join(body_lemmas)]
	print(title_lemmas)
	print(body_lemmas)
	dst = tf.data.Dataset.from_tensor_slices(title_lemmas)
	dsb = tf.data.Dataset.from_tensor_slices(body_lemmas)
	dspred = tf.data.Dataset.zip(((dst, dsb),)).batch(10)
	res = vector_model.predict(dspred)
	ret = {"tags": []}
	for r in np.arange(51):
		if res[0][r]>data['threshold']:
			print("r: ", r, "  value:", res[0][r], " tag: ", mlb.classes_[r])
			ret['tags'] = ret['tags'] + [mlb.classes_[r]] 
	return ret
	

def baseline(data):
	ret = {"tags": []}
	title = data['title'];
	body = data['body'];
	threshold = data['threshold'];
	tv_title = title_vectorizer.transform([title])
	tv_body = body_vectorizer.transform([body])
	for k in title_models.keys():
		if(title_models[k].predict(tv_title)>threshold):
			ret['tags'] = ret['tags'] + [k]
	for k in body_models.keys():
		if(body_models[k].predict(tv_body)>threshold):
			ret['tags'] = ret['tags'] + [k]
	ret['tags'] = list(set(ret['tags']))
	return ret
	
