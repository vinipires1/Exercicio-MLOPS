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
modelo_kmeans = None
modelo_regressao = None
modelo_randomforest = None

@app.route("/", methods=['GET', 'POST'])
def call_home(request = request):
    print(request.values)
    return "SERVER IS RUNNING! \n" + json.dumps({
        "args": str(sys.argv),
    })

@app.route("/modelo_kmeans", methods=['GET', 'POST'])
def call_predict(request=request):
    print(request.values)

    json_ = request.json
    campos = pd.DataFrame(json_)

    cat = ['credit_type', 'age', 'loan_purpose', 'Gender', 'lump_sum_payment']

    label_enconders = {}
    
    for categorical in cat:
            if categorical not in label_enconders:
                label_enconders[categorical] = joblib.load('models/'+categorical+'_label_encoder.joblib')

            campos[categorical] = label_enconders[categorical].transform(campos[categorical])

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    prediction = modelo_kmeans.predict(campos)

    if prediction == 0:
        persona = 'Bronze'
    elif prediction == 1:
        persona = 'Prata'
    else:
        persona = 'Ouro'
    
    ret = {'Cluster': prediction,
           'Persona': persona}

    return app.response_class(response=json.dumps(ret, cls=NpEncoder), mimetype='application/json')
    

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

    cat = ['credit_type', 'age', 'loan_purpose', 'Gender', 'lump_sum_payment']

    label_enconders = {}
    
    for categorical in cat:
            if categorical not in label_enconders:
                label_enconders[categorical] = joblib.load('models/'+categorical+'_label_encoder.joblib')

            campos[categorical] = label_enconders[categorical].transform(campos[categorical])

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    prediction_proba = modelo_regressao.predict_proba(campos)
    
    if prediction_proba <= 0.20:
        fraude_status = 'Baixo Risco'
    elif prediction_proba > 0.20 & prediction_proba <= 0.50:
        fraude_status = 'Médio Risco'
    else:
        fraude_status = 'Grande Risco'
    
    ret = {'Probabilidade de Fraude:': prediction_proba[0][1],
           'Status': fraude_status}
        

    return app.response_class(response=json.dumps(ret, cls=NpEncoder), mimetype='application/json')


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


@app.route("/modelo_randomforest", methods=['GET', 'POST'])
def call_predict(request = request):
    print(request.values)

    json_ = request.json
    campos = pd.DataFrame(json_)

    cat = ['credit_type', 'age', 'loan_purpose', 'Gender', 'lump_sum_payment']

    label_enconders = {}
    
    for categorical in cat:
            if categorical not in label_enconders:
                label_enconders[categorical] = joblib.load( 'models/'+categorical+'_label_encoder.joblib')

            campos[categorical] = label_enconders[categorical].transform(campos[categorical])

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    predict = modelo_randomforest.predict(campos)
    
    if predict == 0:
        classif = 'Adimplente'
    else:
        classif = 'Inadimplente'

    ret = {'Status': predict,
           'Classificação': classif}

    return app.response_class(response=json.dumps(ret, cls=NpEncoder), mimetype='application/json')


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        args.append('models/modelo_randomforest.joblib')
    if len(args) < 2:
        args.append('8080')

    print(args)

    modelo_randomforest = joblib.load(args[0])
    # app.run(port=8080, host='0.0.0.0')
    app.run(port=args[1], host='0.0.0.0')
    pass

