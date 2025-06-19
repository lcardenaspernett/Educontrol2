"""
Modelo Institución para EduControl
Maneja las instituciones educativas del sistema multi-tenant
"""

from datetime import datetime
from app import db
import json

class Institucion(db.Model):
    """Modelo de Institución educativa"""
    
    __tablename__ = 'instituciones'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    nit = db.Column(db.String(20), unique=True, nullable=True)
    direccion = db.Column(db.String(300), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    
    # Configuración visual
    logo = db.Column(db.String(255), nullable=True)  # Ruta del logo
    color_primario = db.Column(db.String(7), default='#007bff')  # Color hex
    color_secundario = db.Column(db.String(7), default='#6c757d')
    
    # Configuración académica
    año_lectivo_activo = db.Column(db.Integer, nullable=False, default=2024)
    parametros_json = db.Column(db.Text, nullable=True)  # JSON con configuraciones personalizadas
    
    # Control de estado
    activa = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Institucion {self.nombre}>'
    
    def get_parametros(self):
        """Obtiene los parámetros como diccionario"""
        if self.parametros_json:
            try:
                return json.loads(self.parametros_json)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_parametros(self, parametros_dict):
        """Establece los parámetros desde un diccionario"""
        self.parametros_json = json.dumps(parametros_dict)
    
    def get_parametro(self, clave, default=None):
        """Obtiene un parámetro específico"""
        parametros = self.get_parametros()
        return parametros.get(clave, default)
    
    def set_parametro(self, clave, valor):
        """Establece un parámetro específico"""
        parametros = self.get_parametros()
        parametros[clave] = valor
        self.set_parametros(parametros)
    
    def to_dict(self):
        """Convierte la institución a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'nit': self.nit,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'logo': self.logo,
            'color_primario': self.color_primario,
            'color_secundario': self.color_secundario,
            'año_lectivo_activo': self.año_lectivo_activo,
            'activa': self.activa,
            'parametros': self.get_parametros()
        }
