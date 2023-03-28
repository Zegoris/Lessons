from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/spaceship.sqlite")
db_sess = db_session.create_session()


def main():
    captain = ["Scott", "Ridley", 21,
               "captain", "research engineer",
               "module_1", "scott_chief@mars.org", "cap"]
    users = [captain]
    for user in users:
        create_user(user)
    captain = [1, "deployment of residential modules 1 and 2",
               15, "2, 3", False]
    jobs = [captain]
    for job in jobs:
        create_job(job)

    app.run()


def create_user(lst):
    global db_sess
    user = User()
    user.surname = lst[0]
    user.name = lst[1]
    user.age = lst[2]
    user.position = lst[3]
    user.speciality = lst[4]
    user.address = lst[5]
    user.email = lst[6]
    user.hashed_password = lst[7]
    db_sess.add(user)
    db_sess.commit()


def create_job(lst):
    global db_sess
    job = Jobs()
    job.team_leader = lst[0]
    job.job = lst[1]
    job.work_size = lst[2]
    job.collaborators = lst[3]
    job.is_finished = lst[4]
    db_sess.add(job)
    db_sess.commit()


if __name__ == '__main__':
    main()