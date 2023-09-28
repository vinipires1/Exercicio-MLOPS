import joblib
import pandas as pd
import json
import numpy as np
from flask import Flask, jsonify, request
import sys

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = NpEncoder
modelo = None

@app.route("/", methods=['GET', 'POST'])
def call_home(request = request):
    print(request.values)
    return "SERVER IS RUNNING! \n" + json.dumps({
        "args": str(sys.argv),
    })

@app.route("/modelo_kmeans", methods=['GET', 'POST'])
def call_predict(request = request):
    print(request.values)

    json_ = request.json
    campos = pd.DataFrame(json_)

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    independentes = ['credit_type', 'Credit_Score', 'income', 'loan_amount', 'age', 'loan_purpose', 'Gender', 'lump_sum_payment']
    
    cat = ['credit_type', 'age', 'loan_purpose', 'Gender', 'lump_sum_payment']

    label_enconders = {}

    for categorical in cat:
        if categorical not in label_enconders:
            label_enconders[categorical] = joblib.load( 'models/'+categorical+'_label_encoder.joblib')

        campos[categorical] = label_enconders[categorical].transform(campos[categorical])

    print("Predizendo para {0} registros".format(campos.shape[0]))

    prediction = modelo_kmeans.predict(campos)
    if isinstance(prediction, int):
        ret = json.dumps({'cluster': prediction}, cls=NpEncoder)

    return app.response_class(response=ret, mimetype='application/json')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        args.append('models/modelo_kmeans.joblib')
    if len(args) < 2:
        args.append('8080')

    print(args)

    modelo_kmeans = joblib.load(args[0])
    # app.run(port=8080, host='0.0.0.0')
    app.run(port=args[1], host='0.0.0.0')
    pass

@app.route("/modelo_regressao", methods=['GET', 'POST'])
def call_predict(request = request):
    print(request.values)

    json_ = request.json
    campos = pd.DataFrame(json_)

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    independentes = ['credit_type', 'Credit_Score', 'income', 'loan_amount', 'age', 'loan_purpose', 'Gender', 'lump_sum_payment', 'cluster']
    
    cat = ['credit_type', 'age', 'loan_purpose', 'Gender', 'lump_sum_payment', 'cluster']

    label_enconders = {}

    for categorical in cat:
        if categorical not in label_enconders:
            label_enconders[categorical] = joblib.load( 'models/'+categorical+'_label_encoder.joblib')

        campos[categorical] = label_enconders[categorical].transform(campos[categorical])

    print("Predizendo para {0} registros".format(campos.shape[0]))

    prediction = modelo_regressao.predict(campos)
    prediction_proba = modelo_regressao.predict_proba(campos)
    if isinstance(prediction, int):
        ret = json.dumps({'Status': prediction,
                          'Probabilidade': prediction_proba}, cls=NpEncoder)


    return app.response_class(response=ret, mimetype='application/json')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        args.append('models/modelo_regressao.joblib')
    if len(args) < 2:
        args.append('8080')

    print(args)

    modelo_regressao = joblib.load(args[0])
    # app.run(port=8080, host='0.0.0.0')
    app.run(port=args[1], host='0.0.0.0')
    pass

