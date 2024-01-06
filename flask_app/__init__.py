from flask import Flask


app = Flask(__name__, '/static')

app.secret_key = 'password'