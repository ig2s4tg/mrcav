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

j1pass = "a2345"
j2pass = "s2345"
j3pass = "d2345"
j4pass = "f2345"
j5pass = "g2345"


"""
      ********************************
      **********   MODELS   **********
      ********************************
"""

class ScoreSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judge = db.Column(db.String(20))
    cont = db.Column(db.String(20))
    finished = db.Column(db.Boolean)

    #Appearance
    a_style = db.Column(db.Integer)
    a_wellg = db.Column(db.Integer)
    a_prof = db.Column(db.Integer)

    #Poise
    p_posture = db.Column(db.Integer)
    p_smile = db.Column(db.Integer)
    p_geye = db.Column(db.Integer)
    p_conf = db.Column(db.Integer)
    p_walk = db.Column(db.Integer)

    #Dance
    d_grace = db.Column(db.Integer)
    d_rythm = db.Column(db.Integer)
    d_smile = db.Column(db.Integer)
    d_conf = db.Column(db.Integer)

    #Talent
    t_creat = db.Column(db.Integer)
    t_tech = db.Column(db.Integer)
    t_exec = db.Column(db.Integer)
    t_over = db.Column(db.Integer)

    #Crowd response
    c_spirit = db.Column(db.Integer)
    c_appl = db.Column(db.Integer)

    def __init__(self, judge, cont):
        self.judge = judge
        self.cont = cont
        self.finished = False
        self.a_style = 0
        self.a_wellg = 0
        self.a_prof = 0
        self.p_posture = 0
        self.p_smile = 0
        self.p_geye = 0
        self.p_conf = 0
        self.p_walk = 0
        self.d_grace = 0
        self.d_rythm = 0
        self.d_smile = 0
        self.d_conf = 0
        self.t_creat = 0
        self.t_tech = 0
        self.t_exec = 0
        self.t_over = 0
        self.c_spirit = 0
        self.c_appl = 0
        db.session.commit()


    #sum each category and multiply by the multiplier
    def calc_a(self): return (self.a_style + self.a_wellg + self.a_prof)                                * 0.2
    def calc_p(self): return (self.p_posture + self.p_smile + self.p_geye + self.p_conf + self.p_walk)  * 0.2
    def calc_d(self): return (self.d_grace + self.d_rythm + self.d_smile + self.d_conf)                 * 0.1
    def calc_t(self): return (self.t_creat + self.t_tech + self.t_exec + self.t_over)                   * 0.4
    def calc_c(self): return (self.c_spirit + self.c_appl)                                              * 0.1

    def calc_total(self):
        return self.calc_a() + self.calc_p() + self.calc_d() + self.calc_t() + self.calc_c()

    def set_a(self, style, wellg, prof):
        self.a_style = style
        self.a_wellg = wellg
        self.a_prof = prof
        db.session.commit()

    def set_p(self, posture, smile, geye, conf, walk):
        self.p_posture = posture
        self.p_smile = smile
        self.p_geye = geye
        self.p_conf = conf
        self.p_walk = walk
        db.session.commit()

    def set_d(self, grace, rythm, smile, conf):
        self.d_grace = grace
        self.d_rythm = rythm
        self.d_smile = smile
        self.d_conf = conf
        db.session.commit()

    def set_t(self, creat, tech, _exec, over): #too late to change it
        self.t_creat = creat
        self.t_tech = tech
        self.t_exec = _exec
        self.t_over = over
        db.session.commit()

    def set_c(self, spirit, appl):
        c_spirit = spirit
        c_appl = appl
        db.session.commit()

    def is_fin(self): #I'm so sorry
        for x in [self.a_style, self.a_wellg, self.a_prof]:
            if (x == 0): return False

        for x in [self.p_posture + self.p_smile + self.p_geye + self.p_conf + self.p_walk]:
            if (x == 0): return False

        for x in [self.d_grace + self.d_rythm + self.d_smile + self.d_conf]:
            if (x == 0): return False

        for x in [self.t_creat + self.t_tech + self.t_exec + self.t_over]:
            if (x == 0): return False

        for x in [self.c_spirit + self.c_appl]:
            if (x == 0): return False

        return True






"""
      *********************************
      **********   ROUTING   **********
      *********************************
"""

@app.route('/', methods=['GET','POST'])
@mobile_template('{mobile/}index.html')
def index(template):
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if (form.login.data == j1pass):
            session["judge"] = "j1"
            flash("Logged in as !", "success")
            return redirect(url_for('cont'))
        elif (form.login.data == j2pass):
            session["judge"] = "j2"
            flash("Logged in as !", "success")
            return redirect(url_for('cont'))
        elif (form.login.data == j3pass):
            session["judge"] = "j3"
            flash("Logged in as !", "success")
            return redirect(url_for('cont'))
        elif (form.login.data == j4pass):
            session["judge"] = "j4"
            flash("Logged in as !", "success")
            return redirect(url_for('cont'))
        elif (form.login.data == j5pass):
            session["judge"] = "j5"
            flash("Logged in as !", "success")
            return redirect(url_for('cont'))
        else:
            flash("incorrect passcode!", "danger")
    return render_template(template, form=form)

@app.route('/contestants/')
@mobile_template('{mobile/}contestants.html')
def cont(template):
    if "judge" in session:
        return render_template(template)
    else:
        return "You need to be logged in to access this page"

@app.route('/score/<name>')
@mobile_template('{mobile/}score.html')
def score(template):

    return render_template(template, form=form)





if __name__ == "__main__":
    app.run(debug=True)