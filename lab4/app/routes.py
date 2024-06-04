from re import findall

from flask import render_template, flash, redirect, url_for 

from src.controller.interpreter import Interpreter, Input
from src.DAO.fileRepository import FileRepository
from commands import commands

from . import app
from .forms import StateForm, CitizenForm, LawForm, ExternalRelationForm, ActionForm, CitizenNameForm

repo = FileRepository('states')
interpreter = Interpreter(commands)


requests = {
    'government': "Government",
    'legislation': "Legislation",
    'external_politics': "External politics",
    'economy': "Economy",
    'population': "Population",
}


def get_states():
    return [state for state in interpreter.interpret(Input("list", []), repo).execute().split('\n') if state]

def get_people(state: str):
    pattern = r"Name: ([A-Z][a-z]* )?([A-Z][a-z]*)"
    return [x[0] + x[1] for x in findall(pattern, interpreter.interpret(Input("list", [state, "population"]), repo).execute())]


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    form = StateForm()
    remove_form = CitizenNameForm()
    remove_form.name.choices = get_states()
    if form.validate_on_submit():
        flash(interpreter.interpret(Input("add", ["state", form.name.data, form.head.data]), repo).execute())
        return redirect(url_for('state', name=form.name.data))
    
    if remove_form.validate_on_submit():
        flash(interpreter.interpret(Input("remove", ["state", remove_form.name.data]), repo).execute())
        return redirect(url_for("index"))
    
    return render_template("index.html", form=form, states=get_states(), remove_form=remove_form)


@app.route('/state/<name>', methods=["GET", "POST"])
def state(name: str):
    citizen_form = CitizenForm()
    if citizen_form.validate_on_submit():
        flash(interpreter.interpret(Input("add", ["citizen", citizen_form.name.data, str(citizen_form.income.data), name]), repo).execute())
        return redirect(url_for("list", state=name, request="population"))
    
    remove_form = CitizenNameForm()
    remove_form.name.choices = get_people(name).copy()
    if remove_form.validate_on_submit():
        print("ffffFFF", remove_form.name.data)
        flash(interpreter.interpret(Input("remove", ["citizen", remove_form.name.data, name]), repo).execute())
        return redirect(url_for("state", name=name))
    
    law_form = LawForm()
    if law_form.validate_on_submit():
        flash(interpreter.interpret(Input("publish_law", [name, law_form.title.data, law_form.text.data]), repo).execute())
        return redirect(url_for("list", state=name, request="legislation"))
    
    rel_form = ExternalRelationForm()
    states = get_states()
    if name in states:
        states.remove(name)
    rel_form.other_state.choices = states
    if rel_form.validate_on_submit():
        flash(interpreter.interpret(Input("create_external_relation", [name, rel_form.other_state.data, rel_form.condition.data]), repo).execute())
        return redirect(url_for("list", state=name, request="external_politics"))
    
    action_form = ActionForm()
    action_form.human.choices = get_people(name).copy()
    print(f'/state/{name}/{action_form.action.data}/{action_form.human.data}')
    if action_form.validate_on_submit():
        print(f'/state/{name}/{action_form.action.data}/{action_form.human.data}')
        return redirect(url_for("human_command", state=name, command=action_form.action.data, human=action_form.human.data))
    
    return render_template(
        'state.html', 
        name=name, 
        requests=requests.items(), 
        citizen_form=citizen_form,
        law_form=law_form,
        rel_form=rel_form,
        action_form=action_form,
        remove_form=remove_form
        )


@app.route('/state/<state>/list/<request>')
def list(request: str, state: str):
    input_ = Input("list", [state, request])
    try:
        command_ = interpreter.interpret(input_, repo)
        answer = command_.execute()
    except Exception as e:
        answer = str(e)
    
    if not command_.can_execute():
        answer = "Command can't execute"

    return render_template(
        'list.html',
        answer=answer,
        request=request,
        name=request.replace('_', ' ').capitalize(),
        state=state
    )
    
@app.route('/state/<state>/<command>')
def command(command: str, state: str):
    input_ = Input(command, [state])
    try:
        command_ = interpreter.interpret(input_, repo)
        answer = command_.execute()
    except Exception as e:
        answer = str(e)
    
    if not command_.can_execute():
        answer = "Command can't execute"

    return render_template(
        'list.html',
        answer=answer,
        request=command,
        name=command.replace('_', ' ').capitalize(),
        state=state
    )
    
@app.route('/state/<state>/<command>/<human>')
def human_command(command: str, state: str, human: str):
    input_ = Input(command, [state, human])
    try:
        command_ = interpreter.interpret(input_, repo)
        answer = command_.execute()
    except Exception as e:
        answer = str(e)
    
    if not command_.can_execute():
        answer = "Command can't execute"

    return render_template(
        'list.html',
        answer=answer,
        request=command,
        name=f"{command.replace('_', ' ').capitalize()} and {human}",
        state=state
    )
