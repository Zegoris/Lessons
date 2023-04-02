from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    age = StringField("Age", validators=[DataRequired()])
    position = StringField("Position")
    speciality = StringField("Speciality")
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')