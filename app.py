from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/content')
def content():
    return render_template('contentpage.html')


    

if __name__ == '__main__':
    app.run(debug=True)