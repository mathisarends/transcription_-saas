from flask import Flask, jsonify, request

app = Flask(__name__)

# Beispiel-Endpunkte
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Willkommen zur API!'})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'data': [1, 2, 3, 4, 5]})

@app.route('/api/data', methods=['POST'])
def post_data():
    payload = request.json
    return jsonify({'received': payload}), 201

if __name__ == '__main__':
    app.run(debug=True)