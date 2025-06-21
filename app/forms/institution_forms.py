# app/forms/institution_forms.py (VERSIÓN CORREGIDA Y COMPLETA)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, RadioField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, Optional, ValidationError, URL
from wtforms.widgets import CheckboxInput, ListWidget

class MultiCheckboxField(SelectMultipleField):
    """Campo personalizado para múltiples checkboxes"""
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class InstitutionCreationForm(FlaskForm):
    """Formulario para crear nueva institución - VERSIÓN COMPLETA Y CORREGIDA"""

    # === 1. INFORMACIÓN BÁSICA ===
    name = StringField('Nombre oficial de la institución',
                      validators=[DataRequired(message="El nombre es obligatorio"), 
                                Length(min=5, max=200, message="El nombre debe tener entre 5 y 200 caracteres")])

    slug = StringField('URL del sistema',
                      validators=[DataRequired(message="El slug es obligatorio"), 
                                Length(min=3, max=50, message="El slug debe tener entre 3 y 50 caracteres"),
                                Regexp(r'^[a-z0-9-]+$', message="Solo letras minúsculas, números y guiones")])

    description = TextAreaField('Descripción breve',
                               validators=[Optional(), Length(max=255, message="Máximo 255 caracteres")])

    # === 2. IDENTIFICACIÓN LEGAL ===
    dane_code = StringField('Código DANE',
                           validators=[DataRequired(message="El código DANE es obligatorio"), 
                                     Length(min=11, max=11, message="Debe contener exactamente 11 dígitos"),
                                     Regexp(r'^[0-9]{11}$', message="Debe contener exactamente 11 dígitos")])

    nit = StringField('NIT',
                     validators=[DataRequired(message="El NIT es obligatorio"), 
                               Length(min=8, max=15, message="El NIT debe tener entre 8 y 15 dígitos")])

    nit_check_digit = StringField('Dígito de verificación',
                                 validators=[DataRequired(message="El dígito de verificación es obligatorio"), 
                                           Length(min=1, max=1, message="Debe ser un solo dígito"),
                                           Regexp(r'^[0-9]$', message="Debe ser un dígito")])

    icfes_code = StringField('Código ICFES',
                            validators=[Optional(), Length(max=20, message="Máximo 20 caracteres")])

    # Resolución de aprobación
    resolution_number = StringField('Número de resolución',
                                   validators=[DataRequired(message="El número de resolución es obligatorio"), 
                                             Length(max=50, message="Máximo 50 caracteres")])

    resolution_date = DateField('Fecha de expedición',
                               validators=[DataRequired(message="La fecha de resolución es obligatoria")])

    resolution_entity = SelectField('Entidad que expide',
                                   choices=[
                                       ('', 'Seleccionar...'),
                                       ('MEN', 'Ministerio de Educación Nacional (MEN)'),
                                       ('SED', 'Secretaría de Educación Departamental'),
                                       ('SEM', 'Secretaría de Educación Municipal'),
                                       ('otra', 'Otra entidad')
                                   ],
                                   validators=[DataRequired(message="Debe seleccionar la entidad que expide")])

    # === 3. UBICACIÓN ===
    department = SelectField('Departamento',
                            choices=[],  # Se llenarán dinámicamente
                            validators=[DataRequired(message="Debe seleccionar un departamento")])

    city = SelectField('Municipio',
                      choices=[('', 'Seleccionar departamento primero')],  # Se llenarán dinámicamente
                      validators=[DataRequired(message="Debe seleccionar un municipio")])

    dane_municipality_code = StringField('Código DANE del municipio',
                                        validators=[DataRequired(message="El código DANE municipal es obligatorio"), 
                                                  Length(min=5, max=5, message="Debe tener exactamente 5 dígitos")],
                                        render_kw={'readonly': True, 'placeholder': 'Se completará automáticamente'})

    zone = RadioField('Zona',
                     choices=[('urbana', 'Urbana'), ('rural', 'Rural')],
                     validators=[DataRequired(message="Debe seleccionar la zona")])

    address = TextAreaField('Dirección exacta',
                           validators=[DataRequired(message="La dirección es obligatoria"), 
                                     Length(max=200, message="Máximo 200 caracteres")])

    neighborhood = StringField('Barrio/Vereda',
                              validators=[DataRequired(message="El barrio/vereda es obligatorio"), 
                                        Length(max=100, message="Máximo 100 caracteres")])

    # === 4. CONTACTO ===
    phone = StringField('Teléfono principal',
                       validators=[DataRequired(message="El teléfono principal es obligatorio"), 
                                 Length(max=20, message="Máximo 20 caracteres")])

    phone_secondary = StringField('Teléfono secundario',
                                 validators=[Optional(), Length(max=20, message="Máximo 20 caracteres")])

    email = StringField('Email institucional',
                       validators=[DataRequired(message="El email institucional es obligatorio"), 
                                 Email(message="Debe ser un email válido"), 
                                 Length(max=120, message="Máximo 120 caracteres")])

    website = StringField('Sitio web',
                         validators=[Optional(), 
                                   URL(message="Debe ser una URL válida"), 
                                   Length(max=200, message="Máximo 200 caracteres")])

    # === 5. INFORMACIÓN ACADÉMICA ===
    sector = RadioField('Sector',
                       choices=[('oficial', 'Oficial'), ('no_oficial', 'No Oficial (Privado)')],
                       validators=[DataRequired(message="Debe seleccionar el sector")])

    character = SelectField('Carácter',
                           choices=[
                               ('', 'Seleccionar...'),
                               ('academico', 'Académico'),
                               ('tecnico', 'Técnico'),
                               ('normalista', 'Normalista'),
                               ('artistico', 'Artístico')
                           ],
                           validators=[DataRequired(message="Debe seleccionar el carácter")])

    levels = MultiCheckboxField('Niveles educativos',
                               choices=[
                                   ('preescolar', 'Preescolar'),
                                   ('primaria', 'Primaria'),
                                   ('secundaria', 'Secundaria'),
                                   ('media', 'Media'),
                                   ('tecnica', 'Técnica')
                               ],
                               validators=[DataRequired(message="Debe seleccionar al menos un nivel educativo")])

    modality = RadioField('Modalidad',
                         choices=[
                             ('presencial', 'Presencial'),
                             ('virtual', 'Virtual'),
                             ('mixta', 'Mixta')
                         ],
                         validators=[DataRequired(message="Debe seleccionar la modalidad")])

    shifts = MultiCheckboxField('Jornadas disponibles',
                               choices=[
                                   ('mañana', 'Mañana'),
                                   ('tarde', 'Tarde'),
                                   ('nocturna', 'Nocturna'),
                                   ('fin_de_semana', 'Fin de semana'),
                                   ('unica', 'Única'),
                                   ('completa', 'Completa')
                               ],
                               validators=[DataRequired(message="Debe seleccionar al menos una jornada")])

    calendar = RadioField('Calendario académico',
                         choices=[
                             ('A', 'Calendario A'),
                             ('B', 'Calendario B'),
                             ('flexible', 'Flexible')
                         ],
                         validators=[DataRequired(message="Debe seleccionar el calendario académico")])

    students_capacity = IntegerField('Capacidad máxima de estudiantes',
                                    validators=[DataRequired(message="La capacidad de estudiantes es obligatoria"), 
                                              NumberRange(min=1, max=50000, message="Debe estar entre 1 y 50,000 estudiantes")])

    campuses_number = IntegerField('Número de sedes',
                                  validators=[DataRequired(message="El número de sedes es obligatorio"), 
                                            NumberRange(min=1, max=100, message="Debe estar entre 1 y 100 sedes")],
                                  default=1)

    operation_start_date = DateField('Fecha de inicio de operaciones',
                                    validators=[DataRequired(message="La fecha de inicio es obligatoria")])

    # === 6. RECTOR/DIRECTOR ===
    director_name = StringField('Nombre completo del director/rector',
                               validators=[DataRequired(message="El nombre del director es obligatorio"), 
                                         Length(min=5, max=120, message="El nombre debe tener entre 5 y 120 caracteres")])

    director_doc_type = SelectField('Tipo de documento',
                                   choices=[
                                       ('', 'Seleccionar...'),
                                       ('CC', 'Cédula de Ciudadanía'),
                                       ('CE', 'Cédula de Extranjería'),
                                       ('PA', 'Pasaporte')
                                   ],
                                   validators=[DataRequired(message="Debe seleccionar el tipo de documento")])

    director_doc_number = StringField('Número de documento',
                                     validators=[DataRequired(message="El número de documento es obligatorio"), 
                                               Length(max=20, message="Máximo 20 caracteres")])

    director_email = StringField('Email del director/rector',
                                validators=[DataRequired(message="El email del director es obligatorio"), 
                                          Email(message="Debe ser un email válido"), 
                                          Length(max=120, message="Máximo 120 caracteres")])

    director_phone = StringField('Teléfono del director/rector',
                                validators=[DataRequired(message="El teléfono del director es obligatorio"), 
                                          Length(max=20, message="Máximo 20 caracteres")])

    director_position = StringField('Cargo',
                                   validators=[DataRequired(message="El cargo es obligatorio"), 
                                             Length(max=50, message="Máximo 50 caracteres")],
                                   default='Rector')

    # === 7. RECURSOS VISUALES ===
    logo = FileField('Logo institucional',
                    validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo archivos JPG y PNG')])

    shield = FileField('Escudo institucional',
                      validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo archivos JPG y PNG')])

    # === 8. PLAN Y CONFIGURACIÓN ===
    plan = RadioField('Plan EduControl',
                     choices=[
                         ('basico', 'Plan Básico - $400.000 COP/mes'),
                         ('estandar', 'Plan Estándar - $600.000 COP/mes'),
                         ('premium', 'Plan Premium - $900.000 COP/mes')
                     ],
                     validators=[DataRequired(message="Debe seleccionar un plan")],
                     default='estandar')

    # === 9. ACEPTACIÓN DE TÉRMINOS ===
    terms_acceptance = BooleanField('Acepto los Términos y Condiciones de EduControl',
                                   validators=[DataRequired(message="Debe aceptar los términos y condiciones")])

    def __init__(self, *args, **kwargs):
        super(InstitutionCreationForm, self).__init__(*args, **kwargs)
        
        # Cargar departamentos dinámicamente
        self.department.choices = self._get_departments()

    def _get_departments(self):
        """Retorna lista de departamentos colombianos"""
        # Lista básica de departamentos - puedes expandir o cargar desde BD
        departments = [
            ('', 'Seleccionar departamento...'),
            ('05', 'Antioquia'),
            ('08', 'Atlántico'),
            ('11', 'Bogotá D.C.'),
            ('13', 'Bolívar'),
            ('15', 'Boyacá'),
            ('17', 'Caldas'),
            ('18', 'Caquetá'),
            ('19', 'Cauca'),
            ('20', 'Cesar'),
            ('23', 'Córdoba'),
            ('25', 'Cundinamarca'),
            ('27', 'Chocó'),
            ('41', 'Huila'),
            ('44', 'La Guajira'),
            ('47', 'Magdalena'),
            ('50', 'Meta'),
            ('52', 'Nariño'),
            ('54', 'Norte de Santander'),
            ('63', 'Quindío'),
            ('66', 'Risaralda'),
            ('68', 'Santander'),
            ('70', 'Sucre'),
            ('73', 'Tolima'),
            ('76', 'Valle del Cauca'),
            ('81', 'Arauca'),
            ('85', 'Casanare'),
            ('86', 'Putumayo'),
            ('88', 'San Andrés y Providencia'),
            ('91', 'Amazonas'),
            ('94', 'Guainía'),
            ('95', 'Guaviare'),
            ('97', 'Vaichada'),
            ('99', 'Vichada')
        ]
        return departments

    def validate_slug(self, field):
        """Validación personalizada para el slug"""
        # Aquí puedes agregar validación para verificar disponibilidad
        # Por ejemplo, consultar la base de datos
        forbidden_slugs = ['admin', 'api', 'www', 'mail', 'ftp', 'blog']
        if field.data.lower() in forbidden_slugs:
            raise ValidationError('Este slug está reservado. Por favor elija otro.')

    def validate_dane_code(self, field):
        """Validación personalizada para el código DANE"""
        # Aquí puedes agregar validación específica del código DANE
        # Por ejemplo, verificar que no esté duplicado en la BD
        pass

    def validate_email(self, field):
        """Validación personalizada para el email institucional"""
        # Verificar que el email no esté en uso
        # Consultar base de datos si es necesario
        pass

    def validate_city(self, field):
        """Validación personalizada para el municipio"""
        if field.data and not self.department.data:
            raise ValidationError('Debe seleccionar un departamento primero.')

    def validate_terms_acceptance(self, field):
        """Validación personalizada para términos y condiciones"""
        if not field.data:
            raise ValidationError('Debe aceptar los términos y condiciones para continuar.')


class InitialSetupForm(FlaskForm):
    """Formulario para configuración inicial de la institución"""

    # Cambio de contraseña obligatorio
    new_password = StringField('Nueva contraseña',
                              validators=[DataRequired(message="La nueva contraseña es obligatoria"), 
                                        Length(min=8, max=128, message="La contraseña debe tener entre 8 y 128 caracteres")])

    confirm_password = StringField('Confirmar contraseña',
                                  validators=[DataRequired(message="Debe confirmar la contraseña")])

    # Configuración básica
    setup_completed = BooleanField('He completado la configuración inicial',
                                  validators=[DataRequired(message="Debe confirmar que completó la configuración")])

    def validate_confirm_password(self, field):
        """Validar que las contraseñas coincidan"""
        if field.data != self.new_password.data:
            raise ValidationError('Las contraseñas no coinciden.')