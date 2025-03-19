from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Service is running!"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    return f"Code received: {code}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
