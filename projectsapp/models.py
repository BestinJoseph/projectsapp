from .extensions import login_manager, db, Session, bcrypt, Entity, Base
from flask_login import UserMixin
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, PickleType
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, pre_load, INCLUDE

@login_manager.user_loader
def load_user(user_id) :
    session = Session()
    return session.query(User).filter_by(id = int(user_id)).first()


class Project(Entity, Base, db.Model) :
    __tablename__ = 'projects'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(100), nullable=False, unique=True)
    project_name = db.Column(db.String(225), nullable=False)
    request_reference = db.Column(db.String(225), nullable=True)
    project_status = db.Column(db.String(50), nullable=False, default="progress")
    
    projects = db.relationship('Proposal', backref=db.backref("projects", lazy=True))

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    client = db.relationship('Client')

    pro_created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def __init__(self, project_id, project_name, request_reference, project_status, pro_created_by, created_by, client_id):
        Entity.__init__(self, created_by)
        self.project_id = project_id
        self.project_name = project_name
        self.request_reference = request_reference
        self.project_status = project_status
        self.client_id = client_id
        self.pro_created_by = pro_created_by

    def __repr__(self) :
        return f"Project( '{self.project_name}', '{self.project_status}', '{self.created_at}', '{self.client_id}' )"


class ProjectSchema(Schema) :
    id = fields.Number()
    project_id = fields.Str()
    project_name = fields.Str()
    request_reference = fields.Str()
    project_status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    client_id = fields.Number()
    pro_created_by = fields.Number()
    last_updated_by = fields.Number()

    class Meta() :
        unknown=INCLUDE
        fields = ('csrf_token', 'submit')

    @pre_load
    def default_project_id(self, data, **kwargs) :
        session = Session()
        last_project = session.query(Project).order_by(Project.created_at.desc()).first()
        session.close()
        if last_project :
            last_project_id = last_project.project_id
        new_id = 'OJCE-RYD-PJT-' + str(int(last_project_id.split('-')[3]) + 1).zfill(3) if last_project else 'OJCE-RYD-PJT-000'
        data['project_id'] = new_id
        return data


class Client(Entity, Base, db.Model) :
    __tablename__ = 'clients'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(200), nullable=False, unique=True)
    client_id = db.Column(db.String(25), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=False)
    telephone = db.Column(db.Integer, nullable=True)
    fax_number = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(50), nullable=False)

    projects = db.relationship('Project', backref=db.backref("clients", lazy=True))
    proposals = db.relationship('Proposal', backref=db.backref("clients", lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def __init__(self, client_name, client_id, address, telephone, fax_number, email, created_by) :
        Entity.__init__(self, created_by)
        self.client_name = client_name
        self.client_id = client_id
        self.address = address
        self.telephone = telephone
        self.fax_number = fax_number
        self.email = email
        self.user_id = created_by

    def __repr__(self) :
        return f"Client( '{self.client_name}', '{self.client_id}', '{self.email}', '{self.created_at}' )"

class ClientSchema(Schema) :
    id = fields.Number()
    client_name = fields.Str()
    client_id = fields.Str()
    address = fields.Str()
    telephone = fields.Integer()
    fax_number = fields.Integer()
    email = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Number()



class User(Entity, Base, UserMixin, db.Model) :
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    clients = db.relationship('Client', backref=db.backref("users", lazy=True))
    projects = db.relationship('Project', backref=db.backref("users", lazy=True))
    
    def __init__(self, username, email, password, created_by) :
        Entity.__init__(self, created_by)
        self.username = username
        self.email = email
        self.password = password

    # def save(self) :
    #     db.session.add(self)
    #     db.session.commit()

    # @staticmethod
    # def get_all() :
    #     return User.query.all()

    # def delete(self) :
    #     db.session.delete(self)
    #     db.session.commit()

    def __repr__(self) :
        return f"User( '{self.username }', '{ self.email }', '{self.created_at}')"


class UserSchema(Schema) :
    id = fields.Number()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Number()
    clients = fields.Nested(ClientSchema, many=True)
    projects = fields.Nested(ProjectSchema, many=True)

    @pre_load
    def hash_password(self, data, **kwargs) :
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8', 'ignore')
        return data

class Proposal(Entity, Base, db.Model) :
    __tablename__ = 'proposals'
    __table_args__ = {'extend_existing': True}

    proposal_id = Column(String())
    proposal_name = Column(String())
    department = Column(Integer())
    request_reference = Column(String())
    approved_by = Column(Integer())
    tests = Column(PickleType)
    total_amount = Column(Integer())
    total_tests = Column(Integer())
    discount = Column(Integer())
    
    # contact_id = Column(Integer(), ForeignKey('contacts.id'))
    # contacts = relationship('Contact')
    contact_id = Column(Integer())

    user_id = Column(Integer(), ForeignKey('users.id'))
    client = relationship('User')

    client_id = Column(Integer(), ForeignKey('clients.id'))
    client = relationship('Client')

    project_id = Column(Integer(), ForeignKey('projects.id'))
    project = relationship('Project')

    # comments = relationship('Comment', backref=backref('proposals', lazy=True))

    def __init__(self, proposal_id, proposal_name, department, request_reference, contact_id, approved_by, tests, total_amount, total_tests, discount, client_id, created_by) :
        Entity.__init__(self, created_by)

        self.department = department
        self.project_id = proposal_id
        self.proposal_name = proposal_name
        self.request_reference = request_reference
        self.contact_id = contact_id
        self.approved_by = approved_by
        self.tests = tests
        self.total_amount = total_amount
        self.total_tests = total_tests
        self.discount = discount
        
    def __repr__(self) :
        return f"( '{self.proposal_id}' '{self.department}' )"

class ProposalSchema(Schema) :
    id = fields.Integer()
    proposal_id = fields.String()
    proposal_name = fields.String()
    department = fields.String()
    request_reference =fields.String()
    contact_id = fields.Integer()
    approved_by = fields.Integer()
    tests = fields.String()
    total_amount = fields.Integer()
    total_tests = fields.Integer()
    discount = fields.Integer()
    user_id = fields.Integer()
    client_id = fields.Integer()
    project_id = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Integer()

    # @pre_load
    # def insert_created_by(self, data, **kwargs) :
    #     pass
