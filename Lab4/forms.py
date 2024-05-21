from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget

from models import Actor, Director, Platform, Script, Studio

class StudioForm(FlaskForm):
    name = StringField('Studio Name', validators=[DataRequired()])
    platforms = SelectMultipleField('Platforms', coerce=int) 
    submit = SubmitField('Add Studio')

    def __init__(self, *args, **kwargs):
        super(StudioForm, self).__init__(*args, **kwargs)
        self.platforms.choices = [(platform.id, platform.platform_name) for platform in Platform.query.all()]

class PlatformForm(FlaskForm):
    platform_type = StringField('Platform Type', validators=[DataRequired()])
    actors = SelectMultipleField('Actor', coerce=int)  # Используем coerce для преобразования в int
    scripts = SelectMultipleField('Scripts', coerce=int)
    directors = SelectMultipleField('Directors', coerce=int)
    submit = SubmitField('Add Platform')

    def __init__(self, *args, **kwargs):
        super(PlatformForm, self).__init__(*args, **kwargs)
        self.actors.choices = [(actor.id, actor.name) for actor in Actor.query.all()]
        self.scripts.choices = [(script.id, script.title) for script in Script.query.all()]
        self.directors.choices = [(director.id, director.name) for director in Director.query.all()]

class ScriptForm(FlaskForm):
    title = StringField('Script Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Script')

class DirectorForm(FlaskForm):
    name = StringField('Director Name', validators=[DataRequired()])
    submit = SubmitField('Add Director')

class ActorForm(FlaskForm):
    name = StringField('Actor Name', validators=[DataRequired()])
    submit = SubmitField('Add Actor')