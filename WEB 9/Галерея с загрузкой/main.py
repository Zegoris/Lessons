from flask import Flask, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
from random import choice
import json
import os

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
list2 = []
for root, dirs, files in os.walk("static/img"):
    for filename in files:
        list2.append("/static/img/" + filename)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)
@app.route('/training/<prof>')
def profession(prof):
    return render_template('prof.html', title=prof, prof=prof)
@app.route('/list_prof/<list>')
def prof_list(list):
    return render_template('list_prof.html', title='Profession list', type=list)
@app.route('/answer')
@app.route('/auto_answer')
def answer():
    with open("settings.json", "rt", encoding="utf8") as f:
        answers = json.loads(f.read())
        answers = answers['answer']
    return render_template('answer.html', title=answers['title'], file=answers)
@app.route('/distribution')
def distr():
    list = ["Ридли Скотт", "Тедди Сандерс", "Энди Уир", "Шон Бин"]
    return render_template('direcrory.html', title='Distribution', list=list)
@app.route('/member')
def choices():
    with open("templates/members.json", "rt", encoding="utf8") as f:
        file = json.loads(f.read())
        file = file['members'][choice(['first', 'second', 'third'])]
    return render_template('card.html', title='Личная карточка', file=file)
@app.route('/galery', methods=['GET', 'POST'])
def training():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            a = len(list2) + 1
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(a) + ".jpg"))
            list2.append("/static/img/" + str(a) + ".jpg")
            print(list2)
            return render_template('galery.html', list=list2[1:], len=len(list2))
    return render_template('galery.html', list=list2[1:], len=len(list2))


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')