from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, TextAreaField, SelectField, FormField, FieldList, Form
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError
from projectsapp.models import User, Client, Project #, Contact
from .extensions import Session


class UserRegistrationForm(FlaskForm) :
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email) :
        session = Session()
        user = session.query(User).filter_by(email = email.data).first()
        session.close()
        if user :
            raise ValidationError('Email you have entered is already exist, please try another.')

    def validate_username(self, username) :
        session = Session()
        user = session.query(User).filter_by(username = username.data).first()
        session.close()
        if user :
            raise ValidationError('Username you have entered is already exist, please try another.')

class UserLoginForm(FlaskForm) :
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')  
    submit = SubmitField('Sign in')

class ClientCreateForm(FlaskForm) :
    clientname = StringField('Client Name', validators=[DataRequired(), Length(min=2, max=120)])
    address = TextAreaField('Address', validators=[DataRequired()])
    telephone = IntegerField('Telephone Number', validators=[DataRequired()])
    faxnumber = IntegerField('Fax Number', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Create Client')

    def validate_clientname(self, clientname) :
        session = Session()
        client = session.query(Client).filter_by(client_name=clientname.data).first()
        session.close()
        if client :
            raise ValidationError('Client already exist, please check with admin')

class ProjectCreateForm(FlaskForm) :
    client_id = SelectField('Client Name')
    project_name = StringField('Project name', validators=[DataRequired(), Length(max=250, min=5)])
    request_reference = StringField('Request Type', validators=[DataRequired()])
    submit = SubmitField('Create Project')

    def __init__(self, *args, **kwargs) :
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        session = Session()
        clients = session.query(Client).all()
        session.close()
        self.client_id.choices = [(str(c.id), c.client_name) for c in clients]

class ProposalTestForm(Form) :
    quantity = IntegerField('Quantity')

class ProposalCreateForm(FlaskForm) :
    project_name = SelectField('Project Name')
    proposal_name = StringField('Proposal Name', validators=[DataRequired(), Length(max=250, min=5)])
    request_reference = StringField('Request Referenc', validators=[DataRequired(), Length(max=250, min=5)])
    contact_id = SelectField('Contact Person')
    tests = FieldList(FormField(ProposalTestForm), min_entries=7, max_entries=7)
    submit = SubmitField('Propose')

    def __init__(self, *args, **kwargs) :
        super(ProposalCreateForm, self).__init__(*args, **kwargs)
        session = Session()
        projects = session.query(Project).order_by(Project.id.desc())
        session = Session()
        self.project_name.choices = [(int(project.id), project.project_name) for project in projects]
        self.contact_id.choices = [(int(cont['do_id']), cont['contact_name']) for cont in [{'do_id': 1, 'contact_name': 'John Doe'}, {'do_id': 2, 'contact_name': 'Merlin Kuma'}]]


