from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# A form class simply defines the fields of the form as class variables.

class SearchForm(FlaskForm):
    vehicle_year = StringField('Vehicle Year', validators=[DataRequired()])
    vehicle_make = StringField('Vehicle Make', validators=[DataRequired()])
    vehicle_model = StringField('Vehicle Model', validators=[DataRequired()])
    submit = SubmitField('Submit')