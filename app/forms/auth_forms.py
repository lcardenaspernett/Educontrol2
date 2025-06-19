"""
Formularios de autenticación
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import Usuario

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    correo = StringField('Correo electrónico', 
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'tu@email.com'})
    
    password = PasswordField('Contraseña', 
                           validators=[DataRequired()],
                           render_kw={'placeholder': 'Contraseña'})
    
    recordar = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    """Formulario de registro de usuario"""
    nombre_completo = StringField('Nombre completo', 
                                validators=[DataRequired(), Length(min=2, max=120)],
                                render_kw={'placeholder': 'Nombre completo'})
    
    correo = StringField('Correo electrónico', 
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'tu@email.com'})
    
    password = PasswordField('Contraseña', 
                           validators=[DataRequired(), Length(min=6)],
                           render_kw={'placeholder': 'Mínimo 6 caracteres'})
    
    password_confirm = PasswordField('Confirmar contraseña',
                                   validators=[DataRequired(), 
                                             EqualTo('password', message='Las contraseñas deben coincidir')],
                                   render_kw={'placeholder': 'Repetir contraseña'})
    
    rol = SelectField('Rol', 
                     choices=[
                         ('estudiante', 'Estudiante'),
                         ('docente', 'Docente'),
                         ('padre', 'Padre/Acudiente'),
                         ('admin_institucional', 'Administrador Institucional')
                     ],
                     validators=[DataRequired()],
                     default='estudiante')
    
    submit = SubmitField('Registrarse')
    
    def validate_correo(self, field):
        """Validar que el correo no esté registrado"""
        usuario = Usuario.query.filter_by(correo=field.data.lower()).first()
        if usuario:
            raise ValidationError('Este correo ya está registrado.')

class ChangePasswordForm(FlaskForm):
    """Formulario para cambiar contraseña"""
    password_actual = PasswordField('Contraseña actual', 
                                  validators=[DataRequired()],
                                  render_kw={'placeholder': 'Contraseña actual'})
    
    password_nueva = PasswordField('Nueva contraseña', 
                                 validators=[DataRequired(), Length(min=6)],
                                 render_kw={'placeholder': 'Nueva contraseña'})
    
    password_confirm = PasswordField('Confirmar nueva contraseña',
                                   validators=[DataRequired(), 
                                             EqualTo('password_nueva', message='Las contraseñas deben coincidir')],
                                   render_kw={'placeholder': 'Repetir nueva contraseña'})
    
    submit = SubmitField('Cambiar Contraseña')
