from flask import Blueprint, render_template, url_for, flash, request, redirect
from projectsapp.forms import UserLoginForm, UserRegistrationForm
from projectsapp.extensions import bcrypt, db, Session
from projectsapp.models import User, UserSchema
from flask_login import login_user, current_user, login_required, logout_user

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def user_register() :
    form = UserRegistrationForm()
    if form.validate_on_submit() :
        session = Session()
        last_user = session.query(User).order_by(User.id.desc()).first()
        session.close()
        print(last_user)
        # if last_user == None :
        #     creator = 1.0
        creator = (last_user.id + 1) if last_user else 1.0
        form_data = {'username': form.username.data, 'email': form.email.data, 'password': form.password.data}
        # postgreSQL inofmation below
        posted_user = UserSchema(only=('username', 'email', 'password')).load(form_data)
        user = User(**posted_user, created_by=creator)
        session = Session()
        session.add(user)
        session.commit()
        
        new_user = UserSchema().dump(user)
        session.close()
        flash('You account has been created successfully', 'success')
        return redirect(url_for('auth_blueprint.user_login'))
    return render_template('register_user.html', title="Register", form=form)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def user_login() :
    if current_user.is_authenticated :
        return redirect( url_for('main_blueprint.home') )
    form = UserLoginForm()
    if form.validate_on_submit() :
        session = Session()
        user = session.query(User).filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) :
            login_user(user, remember=form.remember.data)
            next_route = request.args.get('next')
            return redirect(next_route) if next_route else redirect(url_for('main_blueprint.home'))
        else :
            flash('Your account info are incorrect', 'danger')
    return render_template('login.html', title="User", form=form)

@auth_blueprint.route('/logout')
@login_required
def user_logout() :
    logout_user()
    return redirect( url_for('main_blueprint.home') )

@auth_blueprint.route('/profile')
@login_required
def user_profile() :
    sessions = Session()
    user = sessions.query(User).filter_by(id=current_user.id).first()
    return render_template('user_profile.html', title="Profile", user=user)