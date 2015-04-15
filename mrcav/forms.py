from wtforms import Form, BooleanField, TextField, validators, RadioField

class LoginForm(Form):
    login = TextField('login')

class ScoreForm(Form):
    test = RadioField('test', choices=[('1', 1),('2', 2),('3', 3),('4', 4),('5', 5),('6', 6),('7', 7),('8', 8),('9', 9),('10', 10)])