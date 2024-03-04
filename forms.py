from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TransactionForm(FlaskForm):
    type = SelectField('Type', choices=[('Expense', 'Expense'), ('Income', 'Income')], validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])  # Text input for category name
    submit = SubmitField('Submit')

class BudgetForm(FlaskForm):
    amount = DecimalField('Budget Amount', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])  # Utilize a dropdown in the template if preferred
    timeframe = SelectField('Timeframe', choices=[('Monthly', 'Monthly'), ('Annually', 'Annually')], validators=[DataRequired()])
    submit = SubmitField('Set Budget')
