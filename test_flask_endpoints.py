from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/test/minimal')
def test_minimal():
    return jsonify({'status': 'ok', 'message': 'Flask funciona'})

@app.route('/test/error')
def test_error():
    return jsonify({'error': 'test error'}), 500

if __name__ == '__main__':
    print("Testing Flask básico en puerto 27780...")
    app.run(port=27780, debug=True)
