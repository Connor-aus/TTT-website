from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# form used in basket
class CheckoutForm(FlaskForm):
    firstname = StringField("Your first name", validators=[InputRequired()])
    surname = StringField("Your surname", validators=[InputRequired()])
    avatarname= StringField("Avatar name", validators=[InputRequired()])
    email = StringField("Your email", validators=[InputRequired(), email()])
    submit = SubmitField("Request invoice")

