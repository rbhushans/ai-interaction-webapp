from app import app
from flask import render_template, request, send_file

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/train")
def input():
    return render_template("train.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/train_model", methods=["POST"])
def train_model():
    #train the model
    params = request.data.decode("utf-8") 
    params = params.split(",")
    #train model instead of txt file
    filename = ("_").join(params) +".txt"
    file = open(filename, 'w')
    file.write((" ").join(params))
    file.close()
    try:
        return send_file(filename, attachment_filename=filename)
    except Exception as e:
        return str(e)

@app.route("/test_model", methods=["POST"])
def test_model():
    #test model
    model = request.files['file']
    if model.filename != '':
        model.save(model.filename)
    #do testing with pkl file
    return filename

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

