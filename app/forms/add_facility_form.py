# app/forms/facility_form.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL

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

    image = FileField("Facility Image", validators=[
        FileRequired(),
        FileAllowed(["jpg", "jpeg", "png", "gif", "webp", "avif"], "Images only (jpg, jpeg, png, gif, webp, avif).")
    ])

    address = StringField("Address", validators=[Optional(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    opening_hours = StringField("Opening Hours", validators=[Optional(), Length(max=255)])
    price_range = SelectField("Price Range", choices=[
        ("", "Not specified"),
        ("$", "$ Budget"),
        ("$$", "$$ Moderate"),
        ("$$$", "$$$ Premium"),
        ("$$$$", "$$$$ Luxury"),
    ], validators=[Optional()])
    website = StringField("Website", validators=[Optional(), URL(require_tld=False), Length(max=255)])
    menu_items = TextAreaField("Menu Items", validators=[Optional(), Length(max=2000)])

    submit = SubmitField("Create Facility")
