from app import app
from flask import render_template, request, send_file

app.config['MAX_CONTENT_LEGNTH'] = 1000000000

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
        f = request.files['file']
        print(f) 