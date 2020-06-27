from projectsapp.extensions import Session, Base, Entity
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, pre_load, INCLUDE

class Test(Entity, Base) :
  __tablename__ = "tests"
  __table_args__ = {'extend_existing': True}

  test_name = Column(String())
  test_descripton = Column(Text())
  expiration_date = Column(Date())
  
  department_id = Column(Integer())
  # department_id = Column(Integer(), ForeignKey('department.id'))
  # department = relationship('Department')

  def __init__(self, test_name, test_description, expiration_data, created_by):
    Entity.__init__(self, created_by)
    self.test_name = test_name
    self.test_descripton = test_description
    self.expiration_date = expiration_data

class TestSchema(Schema) :
  id = fields.Integer()
  test_name = fields.String()
  test_description = fields.String()
  expiration_date = fields.Date(format='%Y-%m-%d')
  department_id = fields.Integer()

  class Meta :
    fields = ('test_name', 'test_description', 'expiration_date', 'department_id')
    many=True

test_schema = TestSchema()
test_schema = TestSchema(many=True)