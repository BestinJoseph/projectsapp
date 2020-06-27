from flask_wtf import FlaskForm
from wtforms import Form, DateTimeField, DateField, StringField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField
from projectsapp.extensions import Session

class TestCreateForm(FlaskForm) :
  test_name = StringField('Test Name', validators=[DataRequired(), Length(min=5, max=250)])
  test_description = TextAreaField('Description', validators=[DataRequired()])
  expiration_date = DateField('Expiration Date', validators=[DataRequired()], format = '%Y-%m-%d')
  department_id = SelectField('Department Id')
  submit = SubmitField('Test')

  def __init__(self, *args, **kwargs):
    super(TestCreateForm, self).__init__(*args, **kwargs)
    sessions = Session()
    # departments = sessions.query(Department).order_by(Department.id.desc())
    departments = [{'id': 1, 'department_name': 'Material Testing'}, {'id': 2, 'department_name': 'Chemical Analysis'}, { 'id': 3, 'department_name': 'Geotechnical Investigation'}]
    sessions.close()
    self.department_id.choices = [(str(d['id']), d['department_name']) for d in departments]