# forms.py
from flask_wtf import FlaskForm
from wtforms import FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class RatingForm(FlaskForm):
    service_quality = FloatField("Service quality", validators=[DataRequired(), NumberRange(min=1, max=5)])
    food_quality = FloatField("Food quality", validators=[DataRequired(), NumberRange(min=1, max=5)])
    mood = FloatField("Mood", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField("Comment", validators=[Length(max=500)])
    submit = SubmitField("Add rating")
