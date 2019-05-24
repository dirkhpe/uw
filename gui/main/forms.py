from flask_wtf import FlaskForm
from gui.lib.guidb import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, InputRequired, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RadioList(FlaskForm):
    """
    Generic form to implement radiofield in list.
    """
    itemlist = RadioField('Select Item', validators=[InputRequired()])
    submit = SubmitField('Select')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(_, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class Search(FlaskForm):
    itemlist = RadioField('Select Field', validators=[InputRequired()])
    term = StringField('Term', validators=[DataRequired()])
    submit = SubmitField('Search')
