"""
Rutas de autenticación
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from werkzeug.urls import url_parse
from app import db
from app.models.user import User
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
        # Obtener input del usuario (puede ser email o username)
        login_input = form.correo.data.lower().strip()
        
        # Buscar usuario por email O username
        usuario = User.query.filter(
            or_(
                User.email == login_input,
                User.username == login_input
            )
        ).first()
                
        if usuario and usuario.check_password(form.password.data):
            # Verificar si la cuenta está activa
            if not usuario.is_active:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
                return render_template('auth/login.html', form=form)
                        
            # Actualizar último acceso
            usuario.last_login = datetime.utcnow()
            db.session.commit()
                        
            # Iniciar sesión
            remember_me = getattr(form, 'remember_me', None)
            remember_value = remember_me.data if remember_me else False
            login_user(usuario, remember=remember_value)
                        
            # Redirigir a la página solicitada o al dashboard
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.dashboard')
                        
            flash(f'¡Bienvenido/a {usuario.full_name}!', 'success')
            return redirect(next_page)
        else:
            flash('Email/Usuario o contraseña incorrectos.', 'error')
        
    flash_errors(form)
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    user_name = current_user.full_name
    logout_user()
    flash(f'Has cerrado sesión exitosamente, {user_name}.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """Cambiar contraseña"""
    form = ChangePasswordForm()
        
    if form.validate_on_submit():
        if current_user.check_password(form.password_actual.data):
            current_user.set_password(form.password_nueva.data)
            
            # Actualizar timestamp de modificación
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
                        
            flash('Contraseña actualizada exitosamente.', 'success')
            return redirect(url_for('main.profile'))  # Corregido: main.profile en lugar de main.perfil
        else:
            flash('La contraseña actual es incorrecta.', 'error')
        
    flash_errors(form)
    return render_template('auth/cambiar_password.html', form=form)