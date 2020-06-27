from flask import Blueprint, redirect, render_template, url_for
from projectsapp.extensions import Session
from projectsapp.forms import ProposalCreateForm, ProposalTestForm

proposal_blueprint = Blueprint('proposal_blueprint', __name__, url_prefix='/proposals')

@proposal_blueprint.route('/', methods=['GET'])
def proposal_home() :
    proposals = []
    return render_template('proposals_home.html', proposals=proposals, title="Proposals")

@proposal_blueprint.route('/create', methods=['GET', 'POST'])
def create_proposal() :
    filenames = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']

    form=ProposalCreateForm()
    print(form.data)
    return render_template('create_proposal.html', title="Proposal", form=form)