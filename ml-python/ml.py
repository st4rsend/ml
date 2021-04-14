from flask import Flask, jsonify
from flask_cors import CORS
import os
from joblib import dump, load

model_path = "models/"

title_models = load(model_path + 'top50_title_RidgeC_baseline.joblib')
body_models = load(model_path + 'top50_body_RidgeC_baseline.joblib')
title_vectorizer = load(model_path + 'top50_title_vectorizer.joblib')
body_vectorizer = load(model_path + 'top50_body_vectorizer.joblib')


ret = {
	"tags": [
		"tag1",
		"tag2",
		"tag3"
	]
}

app = Flask(__name__)
# CORS(app)
@app.route('/flask/predict/<string:str_predict>', methods=['GET'])
def predict(str_predict):
	tv_title = title_vectorizer.transform([str_predict])
	tv_body = body_vectorizer.transform([str_predict])
	ret = {"tags": []}
	for k in title_models.keys():
		if(title_models[k].predict(tv_title)>0):
			ret['tags'] = ret['tags'] + [k]
	return jsonify(ret)

@app.route('/flask/models/', methods=['GET'])
def get_models():
	return jsonify({
		'title': [(k,title_models[k].alpha) for k in title_models.keys()],
		'body': [(k,body_models[k].alpha) for k in body_models.keys()],
	})

if __name__ == '__main__':
    app.run(debug=True)
