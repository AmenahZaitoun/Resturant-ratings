from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class RegistrationForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=32)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=32)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=32)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    
    password = PasswordField("Password", validators=[
        DataRequired(),
        Regexp(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$",
            message="Password must be 8-32 characters and include uppercase, lowercase, numbers, and special characters."
        )
    ])
    
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), 
        EqualTo("password", message="Passwords must match.")
    ])
    
    submit = SubmitField("Sign Up")
