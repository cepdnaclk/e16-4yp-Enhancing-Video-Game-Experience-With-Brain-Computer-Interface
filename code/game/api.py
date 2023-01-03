from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_move/<string:x>', methods=['POST'])
def print_move(x):
    move = json.loads(x)
    print(move)
    return('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)