from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import Login, User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from recommender import *
from rec_system import *

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = current_user
    user = User.query.filter_by(username=user.username).first()
    # --- details about user----
    user_details = {
        "username" :user.username,
        "name": user.name,
        "github": user.github,
        "skill": user.skills,

    }
    result = recommender_sys(user.skills)
    # ---------------------------
    return render_template('index.html', repos = result)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Login(username=form.username.data)
        user.set_password(form.password.data)
        data = User(name=form.name.data, username=form.username.data, github=form.github_id.data, skills=form.skill.data)
        db.session.add(data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
