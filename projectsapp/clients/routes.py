from flask import Blueprint, render_template, redirect, url_for, flash, request
from projectsapp.forms import ClientCreateForm
from projectsapp.extensions import bcrypt, db, Session
from projectsapp.models import User, Client, Project, ClientSchema
from flask_login import current_user, login_required
from datetime import datetime

clients_blueprint = Blueprint('clients_blueprint', __name__, url_prefix='/clients')

@clients_blueprint.route('/', methods=['GET'])
@login_required
def clients() :
    sessions = Session()
    clients = sessions.query(Client).all()
    try :
        client_state = []
        for index, client in enumerate(clients):
            client_state.append({'client_name': client.client_name})
            total = len(client.projects)
            total_progress = len([pro for pro in client.projects if pro.project_status == 'progress'])
            total_finished = len([pro for pro in client.projects if pro.project_status == 'finished'])
            client_state[index].update({'projects': total, 'progress': total_progress, 'finished': total_finished})
        return render_template('clients.html', title="Clients", clients=client_state, ex_clients = clients)
    finally :
        sessions.close()

@clients_blueprint.route('/create', methods=['POST', 'GET'])
@login_required
def create_client() :
    form = ClientCreateForm()
    if form.validate_on_submit() :
        session = Session()
        last_client = session.query(Client).order_by(Client.created_at.desc()).first()
        print(last_client)
        if last_client is not None :
            last_client_id = last_client.client_id
        client_number = str(int(last_client_id.split('-')[2]) + 1).zfill(3) if last_client else '001'
        client_id = f"OJCE-{datetime.utcnow().strftime('%Y')}-{client_number}"
        form_data = {'client_name' : form.clientname.data, 'address': form.address.data, 'client_id': client_id, 'telephone': form.telephone.data, 'fax_number': form.faxnumber.data, 'email': form.email.data}
        posted_client = ClientSchema(only=('client_name', 'client_id', 'address', 'telephone', 'fax_number', 'email')).load(form_data)
        client = Client(**posted_client, created_by=current_user.id)
        session.add(client)
        session.commit()

        new_client = ClientSchema().dump(client)
        session.close()
        flash('form has been submitted for ', 'success')
        return redirect( url_for('clients_blueprint.clients') )
    return render_template('create_client.html', title="Clients", form=form)

@clients_blueprint.route('/<string:client_name>')
@login_required
def single_client(client_name) :
    session = Session()
    client = session.query(Client).filter_by(client_name=client_name).first()
    return render_template('single_client.html', title="Client", client=client)