from flask import Blueprint, render_template
from .forms import TestCreateForm
from .models import Test, TestSchema
from projectsapp.extensions import Session
from flask_login import login_required, current_user

test_blueprint = Blueprint('test_blueprint', __name__, url_prefix="/tests")

@test_blueprint.route('/')
def tests_home() :
  tests=[]
  return render_template('test_home.html', title="Tests", tests=tests)

@test_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_test() :
  form=TestCreateForm()
  if form.validate_on_submit() :
    form_data = {
      'test_name': form.test_name.data,
      'test_description': form.test_description.data,
      'expiration_date': form.expiration_date.data,
      'department_id': int(form.department_id.data)
    }
    print(form_data)
    sessions = Session()
    posted_test = TestSchema().load(form_data)
    test = Test(**posted_test, created_by=current_user.id)
    sessions.commit()
    # sending back created test
    new_test = TestSchema(only=('test_name', 'created_by')).dumps(test)
    sessions.close()
    print(new_test)
  return render_template('create_test.html', title="Tests", form=form)