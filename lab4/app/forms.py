from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Regexp, NumberRange


class CitizenForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Regexp(r"^([A-Z][a-z]* )?([A-Z][a-z]*)$", message="Invalide name")])
    income = IntegerField("Income", validators=[DataRequired(), NumberRange(0, None, "Invalide income")])
    submit = SubmitField("Register")
    
class CitizenNameForm(FlaskForm):
    name = SelectField("Name", validators=[DataRequired()])
    submit = SubmitField("Remove")

class ActionForm(FlaskForm):
    human = SelectField("Name", validators=[DataRequired()])
    action = SelectField("Action", validators=[DataRequired()], choices=(
        ("provide_security", "Provide security"),
        ("provide_social_support", "Provide social support")
        )
    )
    submit = SubmitField("DO")

class StateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Regexp(r"((([A-Z][a-z]*) )|of |the )*([A-Z][a-z]*)", message="Invalide name")])
    head = StringField("Head", validators=[DataRequired(), Regexp(r"([A-Z][a-z]* )?([A-Z][a-z]*)", message="Invalide name")])
    submit = SubmitField("Add")
    
class LawForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Publish")
    
class ExternalRelationForm(FlaskForm):
    other_state = SelectField("Other state", [DataRequired()])
    condition = SelectField("Condition", [DataRequired()], choices=("war", "peace", "alliance"))
    submit = SubmitField("Add")
    


    
