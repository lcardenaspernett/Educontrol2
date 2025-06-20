# app/routes/superadmin.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.institution import Institution
from app.models.course import Course
from sqlalchemy import func, extract
from datetime import datetime, timedelta

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_superadmin:
            flash('Acceso denegado. Se requieren permisos de SuperAdmin.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@superadmin_bp.route('/dashboard')
@login_required
@superadmin_required
def dashboard():
    # Estadísticas generales
    stats = {
        'total_institutions': Institution.query.count(),
        'total_users': User.query.filter_by(is_active=True).count(),
        'total_admins': User.query.filter_by(role='admin', is_active=True).count(),
        'total_teachers': User.query.filter_by(role='teacher', is_active=True).count(),
        'total_students': User.query.filter_by(role='student', is_active=True).count(),
        'total_parents': User.query.filter_by(role='parent', is_active=True).count()
    }
    
    # Últimas instituciones creadas
    recent_institutions = Institution.query.order_by(Institution.created_at.desc()).limit(5).all()
    
    return render_template('superadmin/dashboard.html', 
                         stats=stats, 
                         recent_institutions=recent_institutions)

@superadmin_bp.route('/api/user-growth')
@login_required
@superadmin_required
def user_growth_data():
    """Datos para gráfico de crecimiento de usuarios (últimos 6 meses)"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Consulta para obtener registros por mes
    monthly_data = db.session.query(
        extract('year', User.created_at).label('year'),
        extract('month', User.created_at).label('month'),
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date,
        User.is_active == True
    ).group_by(
        extract('year', User.created_at),
        extract('month', User.created_at)
    ).order_by('year', 'month').all()
    
    # Formatear datos para Chart.js
    labels = []
    data = []
    
    for record in monthly_data:
        month_name = datetime(int(record.year), int(record.month), 1).strftime('%B %Y')
        labels.append(month_name)
        data.append(record.count)
    
    return jsonify({
        'labels': labels,
        'datasets': [{
            'label': 'Nuevos Usuarios',
            'data': data,
            'borderColor': 'rgb(142, 45, 226)',
            'backgroundColor': 'rgba(142, 45, 226, 0.1)',
            'tension': 0.4
        }]
    })

@superadmin_bp.route('/institutions')
@login_required
@superadmin_required
def institutions():
    """Lista todas las instituciones"""
    page = request.args.get('page', 1, type=int)
    institutions = Institution.query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('superadmin/institutions.html', institutions=institutions)

@superadmin_bp.route('/institution/create', methods=['GET', 'POST'])
@login_required
@superadmin_required
def create_institution():
    """Crear nueva institución"""
    if request.method == 'POST':
        # Procesar formulario de creación
        institution = Institution(
            name=request.form['name'],
            code=request.form['code'],
            city=request.form['city'],
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            website=request.form.get('website')
        )
        
        try:
            db.session.add(institution)
            db.session.commit()
            flash(f'Institución {institution.name} creada exitosamente', 'success')
            return redirect(url_for('superadmin.institutions'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la institución', 'danger')
    
    return render_template('superadmin/create_institution.html')

@superadmin_bp.route('/users')
@login_required 
@superadmin_required
def users():
    """Gestión de usuarios del sistema"""
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '')
    institution_filter = request.args.get('institution', '')
    
    query = User.query
    
    if role_filter:
        query = query.filter_by(role=role_filter)
    if institution_filter:
        query = query.filter_by(institution_id=institution_filter)
    
    users = query.paginate(page=page, per_page=15, error_out=False)
    institutions = Institution.query.all()
    
    return render_template('superadmin/users.html', 
                         users=users, 
                         institutions=institutions,
                         role_filter=role_filter,
                         institution_filter=institution_filter)

@superadmin_bp.route('/settings')
@login_required
@superadmin_required 
def settings():
    """Configuración global del sistema"""
    return render_template('superadmin/settings.html')