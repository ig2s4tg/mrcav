from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, validators, RadioField

class LoginForm(Form):
    login = TextField('login')

class ScoreForm(Form):

    a_style = RadioField('a_style', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    a_wellg = RadioField('a_wellg', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    a_prof = RadioField('a_prof', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    p_posture = RadioField('p_posture', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    p_smile = RadioField('p_smile', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    p_geye = RadioField('p_geye', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    p_conf = RadioField('p_conf', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    p_walk = RadioField('p_walk', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    d_grace = RadioField('d_grace', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    d_rythm = RadioField('d_rythm', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    d_smile = RadioField('d_smile', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    d_conf = RadioField('d_conf', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    t_creat = RadioField('t_creat', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    t_tech = RadioField('t_tech', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    t_exec = RadioField('t_exec', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    t_over = RadioField('t_over', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    c_spirit = RadioField('c_spirit', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)
    c_appl = RadioField('c_appl', choices=[(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9,'9'),(10, '10')], default=0)