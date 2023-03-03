from flask import Flask, render_template, url_for
import json

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')