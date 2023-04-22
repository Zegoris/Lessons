from forms.user import RegisterForm
from forms.job import JobForm
from forms.login import LoginForm
from forms.department import DepartmentForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session, jobs_api
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from flask import Flask, render_template, redirect, request, make_response, jsonify, abort
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/spaceship.sqlite")
db_sess = db_session.create_session()


def main():
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=8888, host='127.0.0.1')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs)

@app.route("/deplist")
def deplist():
    db_sess = db_session.create_session()
    deps = db_sess.query(Department)
    return render_template("dep_list.html", deps=deps)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            hazard=form.hazard.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        if form.is_finished.data:
            job.end_date = datetime.now()
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Adding a job', action='Adding a Job', form=form)

@app.route('/adddep', methods=['GET', 'POST'])
@login_required
def add_dep():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department(
            chief=form.chief.data,
            title=form.department.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/deplist')
    return render_template('dep.html', title='Adding a department', action='Adding a Department', form=form)

@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.hazard.data = jobs.hazard
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.hazard = form.hazard.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html', title='Edit job', action='Edit job', form=form)

@app.route('/edit_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id,
                                               Department.user == current_user).first()
        if dep:
            form.department.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id,
                                               Department.user == current_user).first()
        if dep:
            dep.title = form.department.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/deplist')
        else:
            abort(404)
    return render_template('dep.html', title='Edit department', action='Edit department', form=form)

@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/delete_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def deps_delete(id):
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).filter(Department.id == id,
                                            Department.user == current_user).first()
    if deps:
        db_sess.delete(deps)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/deplist')


if __name__ == '__main__':
    main()