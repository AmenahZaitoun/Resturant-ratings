# app/forms/facility_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class FacilityForm(FlaskForm):
    facility_name = StringField("Facility Name", validators=[
        DataRequired(), Length(min=2, max=100)
    ])

    facility_type = SelectField("Type", choices=[
        ("restaurant", "Restaurant"),
        ("cafe", "Cafe"),
        ("hotel", "Hotel"),
        ("park", "Park"),
        ("cinema","Cinema")
    ], validators=[DataRequired()])

    facility_category = SelectField("Category", choices=[
        ("luxury", "Luxury"),
        ("budget", "Budget"),
        ("family", "Family"),
        ("child_friendly", "Child-friendly"),
        ("youth_friendly", "Youth-friendly")
    ], validators=[DataRequired()])

    image = StringField("Image Filename", validators=[
        DataRequired(), Length(min=3, max=100)
    ])

    submit = SubmitField("Create Facility")
