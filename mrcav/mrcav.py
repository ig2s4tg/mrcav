from flask import Flask, render_template, redirect, request, session, url_for, flash, jsonify
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

j1pass = "apple1"   #waters
j2pass = "pear2"    #kyle
j3pass = "grape3"   #george
j4pass = "banana4"  #unfried
j5pass = "cherry5"  #guest


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
        self.c_spirit = spirit
        self.c_appl = appl
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

    def serialize(self):
        return {
            'id' : self.id,
            'judge' : self.judge,
            'cont' :  self.cont,
            'finished' :  self.finished,

            #Appearance
            'a_style' :  self.a_style,
            'a_wellg' :  self.a_wellg,
            'a_prof' :  self.a_prof,

            #Poise
            'p_posture' :  self.p_posture,
            'p_smile' :  self.p_smile,
            'p_geye' :  self.p_geye,
            'p_conf' :  self.p_conf,
            'p_walk' :  self.p_walk,

            #Dance
            'd_grace' :  self.d_grace,
            'd_rythm' :  self.d_rythm,
            'd_smile' :  self.d_smile,
            'd_conf' :  self.d_conf,

            #Talent
            't_creat' :  self.t_creat,
            't_tech' :  self.t_tech,
            't_exec' :  self.t_exec,
            't_over' : self.t_over,

            #Crowd response
            'c_spirit ' :  self.c_spirit,
            'c_appl ' :  self.c_appl
        }






"""
      *********************************
      **********   ROUTING   **********
      *********************************
"""

@app.route('/', methods=['GET','POST'])
@mobile_template('{mobile/}index.html')
def index(template):
    if session["judge"]:
        return redirect(url_for('cont'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if (form.login.data == "change_me"):
            session["judge"] = "admin"
            flash("Logged in as admin!", "success")
            return redirect(url_for('totals'))

        elif (form.login.data == j1pass):
            session["judge"] = "waters"
            flash("Logged in as Waters!", "success")
            return redirect(url_for('cont'))

        elif (form.login.data == j2pass):
            session["judge"] = "kyle"
            flash("Logged in as Kyle!", "success")
            return redirect(url_for('cont'))

        elif (form.login.data == j3pass):
            session["judge"] = "george"
            flash("Logged in as George!", "success")
            return redirect(url_for('cont'))

        elif (form.login.data == j4pass):
            session["judge"] = "unfried"
            flash("Logged in as Unfried!", "success")
            return redirect(url_for('cont'))

        elif (form.login.data == j5pass):
            session["judge"] = "guest"
            flash("Logged in as guest judge!", "success")
            return redirect(url_for('cont'))
        else:
            flash("incorrect passcode!", "danger")
    return render_template(template, form=form)

@app.route('/logout/')
@mobile_template('{mobile/}logout.html')
def logout(template):
    if session["judge"]:
        session["judge"] = None
        flash("logged out", "info")
    return redirect(url_for('index'))


@app.route('/contestants/')
@mobile_template('{mobile/}contestants.html')
def cont(template):
    if "judge" in session:
        return render_template(template)
    else:
        return "You need to be logged in to access this page"

@app.route('/score/<name>', methods=['GET','POST'])
@mobile_template('{mobile/}score.html')
def score(template, name):
    form = ScoreForm()
    if request.method == 'POST':
        if ScoreSheet.query.filter_by(judge=session["judge"]).filter_by(cont=name).first() is None:
            new_sheet = ScoreSheet(session["judge"], name)
            db.session.add(new_sheet)
            db.session.commit()

        ScoreSheet.query.filter_by(judge=session["judge"]).filter_by(cont=name).first().set_a(form.a_style.data, form.a_wellg.data, form.a_prof.data)
        ScoreSheet.query.filter_by(judge=session["judge"]).filter_by(cont=name).first().set_p(form.p_posture.data, form.p_smile.data, form.p_geye.data, form.p_conf.data, form.p_walk.data)
        ScoreSheet.query.filter_by(judge=session["judge"]).filter_by(cont=name).first().set_d(form.d_grace.data, form.d_rythm.data, form.d_smile.data, form.d_conf.data)
        ScoreSheet.query.filter_by(judge=session["judge"]).filter_by(cont=name).first().set_t(form.t_creat.data, form.t_tech.data, form.t_exec.data, form.t_over.data)
        ScoreSheet.query.filter_by(judge=session["judge"]).filter_by(cont=name).first().set_c(form.c_spirit.data, form.c_appl.data)
        return redirect(url_for('cont'))

    return render_template(template, form=form)

@app.route('/totals/')
@mobile_template('{mobile/}totals.html')
def totals(template):
    if session["judge"] != "admin":
        return "You don't have permission to access this page. Ask Walter for the passcode"
    data = ScoreSheet.query.all()
    return render_template(template, data=data)

@app.route('/data/<name>')
@mobile_template('{mobile/}data.html')
def data(template, name):
    if ScoreSheet.query.filter_by(judge=session["judge"], cont=name).first():
        return jsonify(ScoreSheet.query.filter_by(judge=session["judge"], cont=name).first().serialize())
    return ""

@app.route('/getdone/')
@mobile_template('{mobile/}done.html')
def getdone(template):

    aakash = False
    andre =  False
    andrew = False
    austin = False
    ben = False
    charlie = False
    chris = False
    colton = False
    connor = False
    paul = False
    pedro = False
    scott = False
    tyler = False

    if ScoreSheet.query.filter_by(judge=session["judge"], cont="aakash").first():
        aakash = ScoreSheet.query.filter_by(judge=session["judge"], cont="aakash").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="andre").first():
        andre =  ScoreSheet.query.filter_by(judge=session["judge"], cont="andre").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="andrew").first():
        andrew = ScoreSheet.query.filter_by(judge=session["judge"], cont="andrew").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="austin").first():
        austin = ScoreSheet.query.filter_by(judge=session["judge"], cont="austin").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="ben").first():
        ben = ScoreSheet.query.filter_by(judge=session["judge"], cont="ben").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="charlie").first():
        charlie = ScoreSheet.query.filter_by(judge=session["judge"], cont="charlie").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="chris").first():
        chris = ScoreSheet.query.filter_by(judge=session["judge"], cont="chris").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="colton").first():
        colton = ScoreSheet.query.filter_by(judge=session["judge"], cont="colton").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="connor").first():
        connor = ScoreSheet.query.filter_by(judge=session["judge"], cont="connor").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="paul").first():
        paul = ScoreSheet.query.filter_by(judge=session["judge"], cont="paul").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="pedro").first():
        pedro = ScoreSheet.query.filter_by(judge=session["judge"], cont="pedro").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="scott").first():
        scott = ScoreSheet.query.filter_by(judge=session["judge"], cont="scott").first().is_fin()
    if ScoreSheet.query.filter_by(judge=session["judge"], cont="tyler").first():
        tyler = ScoreSheet.query.filter_by(judge=session["judge"], cont="tyler").first().is_fin()

    return jsonify({
        'aakash' : aakash,
        'andre'  :  andre,
        'andrew' : andrew,
        'austin' : austin,
        'ben' : ben,
        'charlie' : charlie,
        'chris' : chris,
        'colton' : colton,
        'connor' : connor,
        'paul' : paul,
        'pedro' : pedro,
        'scott' : scott,
        'tyler' : tyler
        }
    )







if __name__ == "__main__":
    app.run(debug=True)