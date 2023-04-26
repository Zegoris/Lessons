from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    department = StringField('Title of department', validators=[DataRequired()])
    chief = StringField("Chief's id", validators=[DataRequired()])
    members = StringField("List of members", validators=[DataRequired()])
    email = EmailField("Department Email", validators=[DataRequired()])
    submit = SubmitField('Save')