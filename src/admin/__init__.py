from flask import Blueprint

admin_ = Blueprint('admin_bp', __name__)

from src.admin import admin_views