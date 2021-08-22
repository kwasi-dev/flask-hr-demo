import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from app import db, bcrypt
from ..models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')
from flask_login import login_user


@bp.route('/register', methods=["POST","GET"])
def register():
    pass

@bp.route('/login', methods=["POST","GET"])
def login():
    if request.method == 'POST':
        formParams = request.form.keys()

        if ('username' in formParams and 'password' in formParams):
            username = request.form['username']
            password = request.form['password']
            remember = 'remember' in formParams

            user = User.query.filter_by(email = username).first()
            if user:
                authSuccessful = bcrypt.check_password_hash(user.password, password)

                if (authSuccessful):
                    login_user(user, remember=remember)
                    additional_claims = {}
                    access_token = create_access_token(user.id)
                    resp = jsonify(access_token=access_token, username=username)
                    resp.set_cookie('access_token_cookie', access_token)
                    return redirect(url_for('dashboard.home'))

        flash("Incorrect credentials", category="login-error")

    return render_template('public/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
