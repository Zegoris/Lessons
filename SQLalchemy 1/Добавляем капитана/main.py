from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/spaceship.sqlite")
db_sess = db_session.create_session()


def main():
    captain = ["Scott", "Ridley", 21,
               "captain", "research engineer",
               "module_1", "scott_chief@mars.org", "cap"]
    astronaut = ["Garden", "Thomas", 23,
                 "handyman", "astronaut",
                 "module_2", "thomas_jef@mars.org", "work"]
    engineer = ["Scoty", "Jess", 22,
                "engineer", "astronomer engineer",
                "module_2", "jessi@mars.org", "astro1234"]
    doctor = ["Sevumyan", "Gabrielle", 26,
              "doctor", "doctor",
              "module_3", "777milan777@mars.org", "qazWSX1234."]
    users = [captain, astronaut, engineer, doctor]
    for user in users:
        create_user(user)

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


if __name__ == '__main__':
    main()