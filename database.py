from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import UserMixin
from cryptography.fernet import Fernet
import os
import base64

db = SQLAlchemy()
bcrypt = Bcrypt()

# ============ ENCRIPTACIÓN DE CONTRASEÑAS ============
SECRET_KEY_ENCRYPT = os.environ.get('ENCRYPT_KEY', 'mi-clave-secreta-de-encriptacion-32bytes')

if len(SECRET_KEY_ENCRYPT) < 32:
    SECRET_KEY_ENCRYPT = SECRET_KEY_ENCRYPT.ljust(32, '0')

key = base64.urlsafe_b64encode(SECRET_KEY_ENCRYPT[:32].encode())
cipher = Fernet(key)

def encriptar_contrasena(contrasena):
    if not contrasena:
        return None
    try:
        return cipher.encrypt(contrasena.encode()).decode()
    except Exception as e:
        print(f"❌ Error al encriptar: {e}")
        return None

def desencriptar_contrasena(contrasena_encriptada):
    if not contrasena_encriptada:
        return None
    try:
        return cipher.decrypt(contrasena_encriptada.encode()).decode()
    except Exception as e:
        print(f"❌ Error al desencriptar: {e}")
        return None

# ============ MODELO DE USUARIO ============
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    contrasena_hash = db.Column(db.String(200), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    es_invitado = db.Column(db.Boolean, default=True)
    token_invitacion = db.Column(db.String(200), unique=True, nullable=True)
    token_expiracion = db.Column(db.DateTime, nullable=True)
    fecha_aceptacion = db.Column(db.DateTime, nullable=True)
    
    def verificar_contrasena(self, contrasena):
        return bcrypt.check_password_hash(self.contrasena_hash, contrasena)
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# ============ MODELO DE LÍDER TÉCNICO ============
class LiderTecnico(db.Model):
    __tablename__ = 'lideres_tecnicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    es_alterno = db.Column(db.Boolean, default=False)
    
    aplicacion_id = db.Column(db.Integer, db.ForeignKey('aplicaciones.id'), nullable=False)
    aplicacion = db.relationship('Aplicacion', backref='lideres', lazy=True)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LiderTecnico {self.nombre} - {"Principal" if not self.es_alterno else "Alterno"}>'

# ============ MODELO DE APLICACIÓN ============
class Aplicacion(db.Model):
    __tablename__ = 'aplicaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    credenciales = db.relationship('Credencial', backref='aplicacion', lazy=True)
    
    def get_lider_principal(self):
        return LiderTecnico.query.filter_by(aplicacion_id=self.id, es_alterno=False).first()
    
    def get_lider_alterno(self):
        return LiderTecnico.query.filter_by(aplicacion_id=self.id, es_alterno=True).first()
    
    def __repr__(self):
        return f'<Aplicacion {self.codigo} - {self.nombre}>'

# ============ MODELO DE CREDENCIAL ============
class Credencial(db.Model):
    __tablename__ = 'credenciales'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_servidor = db.Column(db.String(100), nullable=False, index=True)
    ip = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(200))
    tipo_autenticacion = db.Column(db.String(20), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    
    contrasena = db.Column(db.String(500))
    llave_publica = db.Column(db.Text)
    llave_privada = db.Column(db.Text)
    ruta_archivo_ppk = db.Column(db.String(500))
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    creador = db.relationship('Usuario', backref='credenciales', lazy=True)
    
    aplicacion_id = db.Column(db.Integer, db.ForeignKey('aplicaciones.id'), nullable=True)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_contrasena(self):
        return desencriptar_contrasena(self.contrasena)
    
    def set_contrasena(self, contrasena_plana):
        self.contrasena = encriptar_contrasena(contrasena_plana)
    
    def __repr__(self):
        return f'<Credencial {self.nombre_servidor}>'

# ============ MODELO DE LOG DE AUDITORÍA ============
class LogAuditoria(db.Model):
    __tablename__ = 'logs_auditoria'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='logs', lazy=True)
    accion = db.Column(db.String(100), nullable=False)
    entidad = db.Column(db.String(50), nullable=False)
    entidad_id = db.Column(db.Integer)
    detalles = db.Column(db.Text)
    ip = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LogAuditoria {self.accion} - {self.entidad}>'

# ============ MODELO DE CONFIGURACIÓN DE BACKUP ============
class BackupConfig(db.Model):
    __tablename__ = 'backup_config'
    
    id = db.Column(db.Integer, primary_key=True)
    frecuencia_full = db.Column(db.Integer, default=30)
    frecuencia_incremental = db.Column(db.Integer, default=14)
    hora = db.Column(db.Integer, default=2)
    minuto = db.Column(db.Integer, default=0)
    carpeta_destino = db.Column(db.String(200), default='backups')
    max_backups = db.Column(db.Integer, default=10)
    ultimo_backup_full = db.Column(db.DateTime)
    ultimo_backup_incremental = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=True)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BackupConfig frecuencia_full={self.frecuencia_full} frecuencia_incremental={self.frecuencia_incremental}>'

# ============ MODELO DE LOG DE BACKUP ============
class BackupLog(db.Model):
    __tablename__ = 'backup_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    archivo = db.Column(db.String(200))
    tamaño = db.Column(db.Integer)
    estado = db.Column(db.String(20), default='exitoso')
    mensaje = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BackupLog {self.tipo} - {self.fecha}>'

# ============ MODELO DE TICKET ============
class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_ticket = db.Column(db.String(50), unique=True, nullable=False, index=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    prioridad = db.Column(db.String(20))
    estado = db.Column(db.String(20), default='Abierto')
    
    servidor = db.Column(db.String(100))
    aplicacion_id = db.Column(db.Integer, db.ForeignKey('aplicaciones.id'), nullable=True)
    aplicacion = db.relationship('Aplicacion', backref='tickets', lazy=True)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creador = db.relationship('Usuario', backref='tickets_creados', lazy=True)
    
    def __repr__(self):
        return f'<Ticket {self.numero_ticket}>'

# ============ MODELO DE SESIÓN DE CREDENCIAL ============
class SesionCredencial(db.Model):
    __tablename__ = 'sesiones_credenciales'
    
    id = db.Column(db.Integer, primary_key=True)
    credencial_id = db.Column(db.Integer, db.ForeignKey('credenciales.id'), nullable=False)
    credencial = db.relationship('Credencial', backref='sesiones', lazy=True)
    
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    ticket = db.relationship('Ticket', backref='sesiones', lazy=True)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='sesiones_credenciales', lazy=True)
    
    check_in = db.Column(db.DateTime, default=datetime.utcnow)
    check_out = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='Activa')
    contrasena_usada = db.Column(db.String(500))
    motivo_cierre = db.Column(db.String(200))
    
    fecha_inicio_real = db.Column(db.DateTime)
    fecha_fin_real = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<SesionCredencial {self.id} - Ticket {self.ticket.numero_ticket}>'

# ============ MODELO DE ROTACIÓN DE CONTRASEÑA ============
class RotacionContrasena(db.Model):
    __tablename__ = 'rotaciones_contrasena'
    
    id = db.Column(db.Integer, primary_key=True)
    credencial_id = db.Column(db.Integer, db.ForeignKey('credenciales.id'), nullable=False)
    credencial = db.relationship('Credencial', backref='rotaciones', lazy=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='rotaciones', lazy=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('sesiones_credenciales.id'))
    sesion = db.relationship('SesionCredencial', backref='rotacion', lazy=True)
    
    contrasena_anterior = db.Column(db.String(500))
    contrasena_nueva = db.Column(db.String(500))
    fecha_rotacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RotacionContrasena {self.id} - Credencial {self.credencial_id}>'