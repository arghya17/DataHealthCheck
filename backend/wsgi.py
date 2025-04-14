from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/callback')
def callbackend():
    return requests.get('http://0.0.0.0:5000',timeout=10).text
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
