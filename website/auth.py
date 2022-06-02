from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash(message=f"Привет, {user.nickname}!", category="success")
                
                login_user(user, remember=True)
                
                return redirect(url_for("views.index"))
            else:
                flash(message="Неправильный пароль", category="error")
        else:
            flash(message="Аккич не найден", category="error")
    
    
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        
        if (password == None):
            password = ""
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Такой аккич уже существует', category='error')
        elif (email == None) or (len(email) < 2) or (not "@" in email):
            flash('Неправильная почта', category='error')
        elif (nickname == None) or len(nickname) < 2:
            flash('Неправильный ник', category='error')
        else:
            new_user = User(email=email, nickname=nickname, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Новый аккаунт создан', category='success')
            return redirect(url_for('views.index'))
    
    
    return render_template("register.html", user=current_user)
