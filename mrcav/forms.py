from wtforms import Form, BooleanField, TextField, PasswordField, validators, SelectField

class LoginForm(Form):
    login = TextField('login')

