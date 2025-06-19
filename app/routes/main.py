"""
Rutas principales de la aplicación
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.auth.decorators import login_required_custom

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required_custom
def dashboard():
    """Dashboard principal - usa el template general para todos los roles"""
    return render_template('dashboard.html')

@main_bp.route('/perfil')
@login_required_custom
def perfil():
    """Perfil del usuario"""
    return render_template('perfil.html', usuario=current_user)

@main_bp.route('/ayuda')
def ayuda():
    """Página de ayuda"""
    return render_template('ayuda.html')

@main_bp.route('/acerca')
def acerca():
    """Página acerca de"""
    return render_template('acerca.html')
