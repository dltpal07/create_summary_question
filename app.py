from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import summerization
app = Flask(__name__, static_folder='./templates/static')
sentences_list = []
summary_sentence = ""


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/view')
def view_file():
    return render_template('view.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == "POST":
        f = request.files['file']
        f.save(f'./templates/static/{f.filename}')
        #f.save(secure_filename('./pictures/' + f.filename))
        return render_template("view.html")


@app.route('/create_question')
def create_question():
    global sentences_list
    sentences_list = summerization.get_sentences_list()
    global summary_sentence
    summary_sentence = summerization.get_summary(sentences_list)
    sentences_dict_list = []
    for sent in sentences_list:
        sentences_dict = {'text': sent}
        sentences_dict_list.append(sentences_dict)
    #sentences_list = [{'text': 'hi'}, {'text': 'hello'}]
    return render_template("question.html", value=sentences_dict_list)


@app.route('/create_question_again')
def create_question_again():
    sentences_dict_list = []
    for sent in sentences_list:
        sentences_dict = {'text': sent}
        sentences_dict_list.append(sentences_dict)
    #sentences_list = [{'text': 'hi'}, {'text': 'hello'}]
    return render_template("question.html", value=sentences_dict_list)


@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':

        sent = request.form['text']
        print(sent)
        if sent == summary_sentence[:-1]:
            return render_template('form-action.html', value='True')
        else:
            return render_template('form-action.html', value='False')


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', threaded=False)