from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Title of activity', validators=[DataRequired()])
    team_leader = StringField("Team leader's id", validators=[DataRequired()])
    work_size = StringField("Duration", validators=[DataRequired()])
    collaborators = StringField("List of collaborators", validators=[DataRequired()])
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField('Save')