#!/usr/bin/env python3
"""
✅ SISTEMA MÍNIMO FUNCIONAL - Solo endpoints básicos
"""
from flask import Flask, jsonify
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "active", "system": "Chizhevsky AI Minimal"})

@app.route('/api/status')
def status():
    return jsonify({"status": "ok", "timestamp": "2025-09-21T03:00:00Z"})

def run_flask():
    app.run(host='0.0.0.0', port=27777, debug=False)

if __name__ == '__main__':
    print("🚀 Sistema mínimo iniciado en http://localhost:27777")
    run_flask()
