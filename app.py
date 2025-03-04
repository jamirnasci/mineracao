from flask import Flask, jsonify, request

import rede_final

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def index():
    data = request.json
    b = data.get('balance')
    es = data.get('estimated_salary')
    return jsonify({
        "class": rede_final.predict_customer_class(b, es)
    })

if __name__ == '__main__':
    app.run(debug=True)