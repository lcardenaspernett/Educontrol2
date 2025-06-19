"""
Modelo Usuario para EduControl
Maneja usuarios del sistema con roles multi-tenant
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(UserMixin, db.Model):
    """Modelo de Usuario del sistema"""
    
    __tablename__ = 'usuarios'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contraseña_hash = db.Column(db.String(255), nullable=False)
    
    # Control de roles y estado
    rol = db.Column(db.Enum('admin_general', 'admin_institucional', 'docente', 'estudiante', 'padre', 
                           name='rol_usuario'), nullable=False, default='estudiante')
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    # Multi-tenant
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones.id'), nullable=True)
    
    # Timestamps
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime)
    
    # Relaciones
    institucion = db.relationship('Institucion', backref='usuarios')
    
    def __repr__(self):
        return f'<Usuario {self.correo}>'
    
    def set_password(self, password):
        """Establece la contraseña hasheada"""
        self.contraseña_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.contraseña_hash, password)
    
    def is_admin_general(self):
        """Verifica si es administrador general"""
        return self.rol == 'admin_general'
    
    def is_admin_institucional(self):
        """Verifica si es administrador institucional"""
        return self.rol == 'admin_institucional'
    
    def is_docente(self):
        """Verifica si es docente"""
        return self.rol == 'docente'
    
    def is_estudiante(self):
        """Verifica si es estudiante"""
        return self.rol == 'estudiante'
    
    def can_access_institution(self, institucion_id):
        """Verifica si puede acceder a una institución específica"""
        if self.is_admin_general():
            return True
        return self.institucion_id == institucion_id
    
    def to_dict(self):
        """Convierte el usuario a diccionario"""
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'correo': self.correo,
            'rol': self.rol,
            'activo': self.activo,
            'institucion_id': self.institucion_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None
        }
