"""
Rutas de autenticación
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.user import Usuario
from app.forms.auth_forms import LoginForm, ChangePasswordForm
from app.utils.helpers import flash_errors

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=form.correo.data.lower()).first()
        
        if usuario and usuario.check_password(form.password.data):
            if not usuario.activo:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
                return render_template('auth/login.html', form=form)
            
            # Actualizar último acceso
            usuario.ultimo_acceso = datetime.utcnow()
            db.session.commit()
            
            # Iniciar sesión
            login_user(usuario, remember=form.recordar.data)
            
            # Redirigir a la página solicitada o al dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            
            flash(f'¡Bienvenido/a {usuario.nombre_completo}!', 'success')
            return redirect(next_page)
        else:
            flash('Correo o contraseña incorrectos.', 'error')
    
    flash_errors(form)
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """Cambiar contraseña"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.password_actual.data):
            current_user.set_password(form.password_nueva.data)
            db.session.commit()
            
            flash('Contraseña actualizada exitosamente.', 'success')
            return redirect(url_for('main.perfil'))
        else:
            flash('La contraseña actual es incorrecta.', 'error')
    
    flash_errors(form)
    return render_template('auth/cambiar_password.html', form=form)
