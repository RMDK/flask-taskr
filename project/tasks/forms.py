# forms.py

from flask_wtf import Form
from wtforms import TextField, DateField, \
    SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddTaskForm(Form):
    # task_id = IntegerField('Priority')
    name = TextField('', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    due_date = DateField('',
        validators=[DataRequired()], format='%m-%d-%Y'
    )
    priority = SelectField(
        '',
        validators=[DataRequired()],
        choices=[
            ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')
        ]
    )
    # status = IntegerField('Status')
    submit = SubmitField('Submit')