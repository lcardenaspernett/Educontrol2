"""
Rutas principales de la aplicación
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.auth.decorators import login_required_custom

main_bp = Blueprint('main', __name__)

"""
Rutas principales de la aplicación
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.auth.decorators import login_required_custom

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal - muestra bienvenida o redirige según autenticación"""
    if current_user.is_authenticated:
        # Usuario autenticado - redirigir al dashboard apropiado
        if current_user.role == 'superadmin':
            return redirect(url_for('main.dashboard'))  # Por ahora usar dashboard general
        elif current_user.role == 'admin':
            return redirect(url_for('main.dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('main.dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('main.dashboard'))  # Dashboard por defecto
    
    # Usuario no autenticado - mostrar página de bienvenida  
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required_custom
def dashboard():
    """Dashboard principal - usa el template general para todos los roles"""
    return render_template('dashboard.html')

@main_bp.route('/profile')  # Cambiado de /perfil a /profile para consistencia
@login_required_custom
def profile():
    """Perfil del usuario"""
    return render_template('profile.html', usuario=current_user)

# Mantener /perfil por compatibilidad hacia atrás
@main_bp.route('/perfil')
@login_required_custom
def perfil():
    """Perfil del usuario (ruta en español, redirige a profile)"""
    return redirect(url_for('main.profile'))

@main_bp.route('/settings')
@login_required_custom
def settings():
    """Configuración del usuario"""
    return render_template('settings.html', usuario=current_user)

@main_bp.route('/ayuda')
def ayuda():
    """Página de ayuda"""
    return render_template('ayuda.html')

@main_bp.route('/acerca')
def acerca():
    """Página acerca de"""
    return render_template('acerca.html')