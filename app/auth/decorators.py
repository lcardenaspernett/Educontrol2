"""
Decoradores para control de acceso y autorización
"""

from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user, login_required

def require_role(*roles):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados
    Uso: @require_role('admin_general', 'admin_institucional')
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            if not current_user.activo:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
                return redirect(url_for('auth.login'))
            
            if current_user.rol not in roles:
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """
    Decorador que requiere rol de administrador (general o institucional)
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.activo:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
            return redirect(url_for('auth.login'))
        
        if not (current_user.is_admin_general() or current_user.is_admin_institucional()):
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def same_institution_required(f):
    """
    Decorador que requiere que el usuario pertenezca a la misma institución
    o sea administrador general
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.activo:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
            return redirect(url_for('auth.login'))
        
        # Los admin generales pueden acceder a todo
        if current_user.is_admin_general():
            return f(*args, **kwargs)
        
        # Verificar institución si se proporciona en los argumentos
        institucion_id = kwargs.get('institucion_id')
        if institucion_id and not current_user.can_access_institution(institucion_id):
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def login_required_custom(f):
    """
    Decorador personalizado para login que incluye verificación de cuenta activa
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.activo:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function
