from flask import Flask

app = Flask(__name__)

app.secret_key = 'nh98c329812m3400d1' # ! CHANGE LATER TO AN env FILE WITH RANDOMLY GENERATED LARGE STRING NOT IN THIS FILE

from app import screens