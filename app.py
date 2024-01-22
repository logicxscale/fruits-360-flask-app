import os

from flask import Flask, redirect, url_for, send_from_directory
from flask import render_template, request
from werkzeug.utils import secure_filename

from process import predict_image

app = Flask(__name__)

APP_ROOT = app.root_path
target = os.path.join(APP_ROOT, 'temp/')

@app.before_request
def check_for_refresh():
    if request.method == 'GET' and request.referrer == request.url:  # Check for refresh
        for root, dirs, files in os.walk(target, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            return redirect(url_for('index'))  # Redirect to avoid multiple deletions

@app.route("/")
def index():
    return render_template('index.html',title='Home')

@app.route('/about')
def about():
    return render_template('about.html',title='About',name='@bagusa4')

@app.route("/predict")
def predict():
    return render_template("predict.html",title="Predict")

@app.route('/temp/<filename>')
def download_file(filename):
    return send_from_directory(target, filename)

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == 'POST':
        file = request.files['img'] # 'img' is the id passed in input file form field
        filename = file.filename
        file.save("".join([target, filename])) #saving file in temp folder
        print("upload Completed") #printing on terminal

        return redirect(url_for('result', filename=filename))

@app.route("/result/<filename>", methods=["GET","POST"])
def result(filename):
    if (filename == 'null'):
        return redirect(url_for('predict'))
    else:   
        file = "".join([target, filename])
        #imported process.py
        x=predict_image(file) #imported from process file    
        results = [x, "/temp/{}".format(filename)]
        return render_template("result.html",title="Result",results=results)