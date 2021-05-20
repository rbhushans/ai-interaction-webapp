from modelCleaner import cleaner
from app import app
from app import model
from flask import render_template, request, send_file, Response, stream_with_context, session
import pickle
import os
import string
import random
import threading
import asyncio

app.config['MAX_CONTENT_LEGNTH'] = 1000000000

@app.before_first_request
def start_cleaner():
    x = threading.Thread(target=cleaner, args=(), daemon=True)
    x.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/train")
def input():
    return render_template("train.html")

@app.route("/results")
def results():
    if 'file_name' in session:
        temp_file = open(session['file_name'], 'rb')
        temp_file.read(1) # Just to change access time for cleaner process
        temp_file.close()
    return render_template("results.html")

@app.route("/train_model", methods=["POST"])
def train_model():
    #train the model
    params = request.data.decode("utf-8") 
    params = params.split(",")
    # Create 'unique' filename for the user to index
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(32))

    filename, precision, recall = model.construct_lr_model(params, result_str)
    print("Model created with features", params, "and precision =", precision, " and recall =", recall)
    # ! Session database test
    session['file_name'] = filename # Save to session of user (locally on server)

    return filename + "|" + str(precision) + "|" + str(recall)

@app.route("/test_model", methods=["POST"])
def test_model():
    #test model
    #model = request.files['file']
    #if model.filename != '':
    #    model.save(model.filename)
    if 'file_name' in session:
        # Send model into test
        # Retrieve model by doing following:
        # temp_file = open(session['file_name'], 'rb')
        # modelFile = pickle.load(temp_file)
        # temp_file.close()
        # Then use modelFile as a parameter to the model testing 
        print(session['file_name'])
        return session['file_name']
    else:
        # No model trained yet, send error
        return 404

    #do testing with pkl file
    return filename

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ! Tests for DB
@app.route("/database")
def database():

    return render_template("database.html")

@app.route('/database/model', methods=["GET", "POST"])
def getDatabase():
    if request.method == "GET":
        # Send the pkl file to the client browser
        return send_file('../model/all_feat_model.pkl', attachment_filename='all_feat_model.pkl');
    if request.method == "POST":
        # Download the pkl file from the client browser
        f = open('../tmp/temp_model.pkl', 'wb')
        f.write(request.body)
        f.close()
        return "Binary message written!"