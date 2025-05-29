from flask import Blueprint, render_template, redirect, url_for
from flask_security import current_user
from flask_security.utils import url_for_security

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for_security('login'))
    return render_template('index.html')
