from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
from werkzeug.security import generate_password_hash, \
     check_password_hash

from forms import *

app = Flask(__name__)
Mobility(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mrcav.db'
db = SQLAlchemy(app)

app.secret_key = 'QWERTYUIOPASDFGHJKLZXCVBNM'


"""
      ********************************
      **********   MODELS   **********
      ********************************
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    pwhash = db.Column(db.Binary(20)) #use hex and unhex
    schedID = db.Column(db.ForeignKey('schedule.id'))

    def __init__(self, first, last, mail, pw):
        self.firstname = first
        self.lastname = last
        self.email = mail
        self.pwhash = generate_password_hash(pw)
        self.schedID = 0;

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    def set_schedule(self, id):
        self.schedID = id
        db.session.commit()


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period1 = db.Column(db.ForeignKey('class.id'))
    period2 = db.Column(db.ForeignKey('class.id'))
    period3 = db.Column(db.ForeignKey('class.id'))
    period4 = db.Column(db.ForeignKey('class.id'))
    period5 = db.Column(db.ForeignKey('class.id'))
    period6 = db.Column(db.ForeignKey('class.id'))
    period7 = db.Column(db.ForeignKey('class.id'))

    def __init__(self, fir, sec, thi, fou, fif, six, sev):
        self.period1 = fir
        self.period2 = sec
        self.period3 = thi
        self.period4 = fou
        self.period5 = fif
        self.period6 = six
        self.period7 = sev

    def change_sched(self, fir, sec, thi, fou, fif, six, sev):
        self.period1 = fir
        self.period2 = sec
        self.period3 = thi
        self.period4 = fou
        self.period5 = fif
        self.period6 = six
        self.period7 = sev


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(20))
    classname = db.Column(db.String(30))
    dif = db.Column(db.String(10))
    period = db.Column(db.Integer)

    def __init__(self, teach, cn, df, per):
        self.teacher = teach
        self.classname = cn
        self.dif = df
        self.period = per

"""
      *********************************
      **********   ROUTING   **********
      *********************************
"""

@app.route('/')
@mobile_template('{mobile/}index.html')
def index(template):
    form = LoginForm(request.form)
    return render_template(template, form=form)





if __name__ == "__main__":
    app.run(debug=True)