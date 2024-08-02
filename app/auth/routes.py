from flask import Blueprint
from app.auth.views import signup, login, logout, reset_password, change_password

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/logout', methods=['POST'])(logout)
auth_bp.route('/reset-password', methods=['POST'])(reset_password)
auth_bp.route('/change-password', methods=['POST'])(change_password)
