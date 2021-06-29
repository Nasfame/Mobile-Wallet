from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash as genr, check_password_hash as checkr

from app.models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username, __pass__ = data.get('username'), data.get('password')
    user = User.query.filter(User.username == username).first_or_404("Invalid User")

    if checkr(user.password, __pass__):
        login_user(user, remember=True)
    else:
        return jsonify("Invalid Password")

    return jsonify("Login Successful")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify("Logout")


@auth.route('/signup', methods=['POST'])
def sign_up():
    data = request.json

    try:
        username, __pass__ = data["username"], data["password"]
    except:
        return jsonify("Invalid Username || Password")

    user = User.query.filter_by(username=username).first()

    if user is not None:
        return jsonify("User Exists")

    sign_up_bonus = 5000
    hashed_password = genr(__pass__, method='sha256')
    new_user = User(username=username, password=hashed_password, balance=sign_up_bonus)
    db.session.add(new_user)
    db.session.commit()
    return jsonify("User created")
