"""Script para llenar la base de datos con datos de prueba"""
from app import app, db
from database import Usuario, Aplicacion, Credencial, LiderTecnico
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def seed():
    print("🔄 Iniciando seed de base de datos...")
    
    with app.app_context():
        print("🔄 Limpiando base de datos...")
        db.drop_all()
        db.create_all()
        print("✅ Base de datos recreada")
        
        # ===== CREAR USUARIO ADMIN =====
        print("👤 Creando usuario administrador...")
        admin = Usuario(
            nombre='Administrador',
            email='admin@gestor.com',
            contrasena_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            es_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("   ✅ Admin creado: admin@gestor.com / admin123")
        
        # ===== CREAR APLICACIONES CON LÍDERES =====
        print("📱 Creando aplicaciones y líderes técnicos...")
        
        aplicaciones_data = [
            {
                'codigo': 'SFR', 'nombre': 'Salesforce', 'descripcion': 'CRM Salesforce',
                'lider_principal': {'nombre': 'Juan Pérez', 'email': 'juan.perez@empresa.com', 'telefono': '+56 9 1234 5678'},
                'lider_alterno': {'nombre': 'María González', 'email': 'maria.gonzalez@empresa.com', 'telefono': '+56 9 8765 4321'}
            },
            {
                'codigo': 'CON', 'nombre': 'Conectividad', 'descripcion': 'Infraestructura de Conectividad',
                'lider_principal': {'nombre': 'Carlos Rodríguez', 'email': 'carlos.rodriguez@empresa.com', 'telefono': '+56 9 2345 6789'},
                'lider_alterno': {'nombre': 'Ana Martínez', 'email': 'ana.martinez@empresa.com', 'telefono': '+56 9 9876 5432'}
            },
            {
                'codigo': 'RDD', 'nombre': 'RDD', 'descripcion': 'Aplicación RDD',
                'lider_principal': {'nombre': 'Luis Fernández', 'email': 'luis.fernandez@empresa.com', 'telefono': '+56 9 3456 7890'},
                'lider_alterno': {'nombre': 'Elena Soto', 'email': 'elena.soto@empresa.com', 'telefono': '+56 9 0987 6543'}
            },
            {
                'codigo': 'IDE', 'nombre': 'Identidad', 'descripcion': 'Gestión de Identidad',
                'lider_principal': {'nombre': 'Miguel Ángel', 'email': 'miguel.angel@empresa.com', 'telefono': '+56 9 4567 8901'},
                'lider_alterno': {'nombre': 'Laura Reyes', 'email': 'laura.reyes@empresa.com', 'telefono': '+56 9 1098 7654'}
            },
            {
                'codigo': 'SYN', 'nombre': 'Synergia', 'descripcion': 'Synergia 5.0',
                'lider_principal': {'nombre': 'Marcos Neyra', 'email': 'marco.neyra@pluz.pe', 'telefono': '+51 960 407 747'},
                'lider_alterno': {'nombre': 'Sofía Vargas', 'email': 'sofia.vargas@empresa.com', 'telefono': '+51 987 654 321'}
            },
            {
                'codigo': 'OPE', 'nombre': 'Operaciones', 'descripcion': 'Operaciones',
                'lider_principal': {'nombre': 'Roberto Díaz', 'email': 'roberto.diaz@empresa.com', 'telefono': '+56 9 5678 9012'},
                'lider_alterno': {'nombre': 'Paula Rojas', 'email': 'paula.rojas@empresa.com', 'telefono': '+56 9 2109 8765'}
            },
            {
                'codigo': 'APW', 'nombre': 'App Web', 'descripcion': 'Aplicaciones Web',
                'lider_principal': {'nombre': 'Jorge Castillo', 'email': 'jorge.castillo@empresa.com', 'telefono': '+56 9 6789 0123'},
                'lider_alterno': {'nombre': 'Cecilia Molina', 'email': 'cecilia.molina@empresa.com', 'telefono': '+56 9 3210 9876'}
            },
            {
                'codigo': 'ADL', 'nombre': 'Administrador de Lecturas', 'descripcion': 'Lecturas',
                'lider_principal': {'nombre': 'Andrés Herrera', 'email': 'andres.herrera@empresa.com', 'telefono': '+56 9 7890 1234'},
                'lider_alterno': {'nombre': 'Daniela Castro', 'email': 'daniela.castro@empresa.com', 'telefono': '+56 9 4321 0987'}
            },
            {
                'codigo': 'CDP', 'nombre': 'Cloudera', 'descripcion': 'Big Data',
                'lider_principal': {'nombre': 'Patricio Silva', 'email': 'patricio.silva@empresa.com', 'telefono': '+56 9 8901 2345'},
                'lider_alterno': {'nombre': 'Valentina Ruiz', 'email': 'valentina.ruiz@empresa.com', 'telefono': '+56 9 5432 1098'}
            },
            {
                'codigo': 'POL', 'nombre': 'Poliweb', 'descripcion': 'Poliweb',
                'lider_principal': {'nombre': 'Cristian Mena', 'email': 'cristian.mena@empresa.com', 'telefono': '+56 9 9012 3456'},
                'lider_alterno': {'nombre': 'Francisca Acuña', 'email': 'francisca.acuna@empresa.com', 'telefono': '+56 9 6543 2109'}
            },
            {
                'codigo': 'QDA', 'nombre': 'Quenda', 'descripcion': 'Quenda',
                'lider_principal': {'nombre': 'Eduardo Tapia', 'email': 'eduardo.tapia@empresa.com', 'telefono': '+56 9 0123 4567'},
                'lider_alterno': {'nombre': 'Gabriela Muñoz', 'email': 'gabriela.munoz@empresa.com', 'telefono': '+56 9 7654 3210'}
            },
            {
                'codigo': 'BBT', 'nombre': 'Bitbucket', 'descripcion': 'Repositorio',
                'lider_principal': {'nombre': 'Fernando Barra', 'email': 'fernando.barra@empresa.com', 'telefono': '+56 9 1234 5678'},
                'lider_alterno': {'nombre': 'Isidora Lagos', 'email': 'isidora.lagos@empresa.com', 'telefono': '+56 9 8765 4321'}
            },
            {
                'codigo': 'AFC', 'nombre': 'ERP AFC', 'descripcion': 'ERP',
                'lider_principal': {'nombre': 'Gonzalo Cáceres', 'email': 'gonzalo.caceres@empresa.com', 'telefono': '+56 9 2345 6789'},
                'lider_alterno': {'nombre': 'Javiera Pardo', 'email': 'javiera.pardo@empresa.com', 'telefono': '+56 9 9876 5432'}
            },
            {
                'codigo': 'SUP', 'nombre': 'Suprema', 'descripcion': 'Seguridad',
                'lider_principal': {'nombre': 'Héctor Cifuentes', 'email': 'hector.cifuentes@empresa.com', 'telefono': '+56 9 3456 7890'},
                'lider_alterno': {'nombre': 'Katherine Riquelme', 'email': 'katherine.riquelme@empresa.com', 'telefono': '+56 9 0987 6543'}
            },
            {
                'codigo': 'VOT', 'nombre': 'Votaciones', 'descripcion': 'Sistema de Votaciones',
                'lider_principal': {'nombre': 'Ignacio Moya', 'email': 'ignacio.moya@empresa.com', 'telefono': '+56 9 4567 8901'},
                'lider_alterno': {'nombre': 'Lorena Barrera', 'email': 'lorena.barrera@empresa.com', 'telefono': '+56 9 1098 7654'}
            },
            {
                'codigo': 'WCT', 'nombre': 'Web de Contratistas', 'descripcion': 'Contratistas',
                'lider_principal': {'nombre': 'Javier Araya', 'email': 'javier.araya@empresa.com', 'telefono': '+56 9 5678 9012'},
                'lider_alterno': {'nombre': 'Marcela Parra', 'email': 'marcela.parra@empresa.com', 'telefono': '+56 9 2109 8765'}
            },
            {
                'codigo': 'CSE', 'nombre': 'CSE', 'descripcion': 'CSE',
                'lider_principal': {'nombre': 'Karla Escobar', 'email': 'karla.escobar@empresa.com', 'telefono': '+56 9 6789 0123'},
                'lider_alterno': {'nombre': 'Nicolás Fuentes', 'email': 'nicolas.fuentes@empresa.com', 'telefono': '+56 9 3210 9876'}
            },
            {
                'codigo': 'PME', 'nombre': 'PME', 'descripcion': 'PME',
                'lider_principal': {'nombre': 'Leonardo Villalón', 'email': 'leonardo.villalon@empresa.com', 'telefono': '+56 9 7890 1234'},
                'lider_alterno': {'nombre': 'Olga Ramírez', 'email': 'olga.ramirez@empresa.com', 'telefono': '+56 9 4321 0987'}
            },
            {
                'codigo': 'SCA', 'nombre': 'Suite Cartografica', 'descripcion': 'GIS',
                'lider_principal': {'nombre': 'Mauricio Salgado', 'email': 'mauricio.salgado@empresa.com', 'telefono': '+56 9 8901 2345'},
                'lider_alterno': {'nombre': 'Pamela Troncoso', 'email': 'pamela.troncoso@empresa.com', 'telefono': '+56 9 5432 1098'}
            },
            {
                'codigo': 'CTC', 'nombre': 'Contact Center', 'descripcion': 'Contact Center',
                'lider_principal': {'nombre': 'Nelson Cárdenas', 'email': 'nelson.cardenas@empresa.com', 'telefono': '+56 9 9012 3456'},
                'lider_alterno': {'nombre': 'Rosa Márquez', 'email': 'rosa.marquez@empresa.com', 'telefono': '+56 9 6543 2109'}
            },
            {
                'codigo': 'PLA', 'nombre': 'Plataformado', 'descripcion': 'Plataformado',
                'lider_principal': {'nombre': 'Oscar Rivas', 'email': 'oscar.rivas@empresa.com', 'telefono': '+56 9 0123 4567'},
                'lider_alterno': {'nombre': 'Sara Torres', 'email': 'sara.torres@empresa.com', 'telefono': '+56 9 7654 3210'}
            }
        ]
        
        for app_data in aplicaciones_data:
            # Crear aplicación
            if not Aplicacion.query.filter_by(codigo=app_data['codigo']).first():
                nueva_app = Aplicacion(
                    codigo=app_data['codigo'],
                    nombre=app_data['nombre'],
                    descripcion=app_data['descripcion'],
                    activo=True
                )
                db.session.add(nueva_app)
                db.session.flush()  # Para obtener el ID
                
                # Crear líder principal
                lider_principal = app_data['lider_principal']
                nuevo_lider = LiderTecnico(
                    nombre=lider_principal['nombre'],
                    email=lider_principal['email'],
                    telefono=lider_principal['telefono'],
                    es_alterno=False,
                    aplicacion_id=nueva_app.id
                )
                db.session.add(nuevo_lider)
                
                # Crear líder alterno
                lider_alterno = app_data['lider_alterno']
                nuevo_alterno = LiderTecnico(
                    nombre=lider_alterno['nombre'],
                    email=lider_alterno['email'],
                    telefono=lider_alterno['telefono'],
                    es_alterno=True,
                    aplicacion_id=nueva_app.id
                )
                db.session.add(nuevo_alterno)
        
        db.session.commit()
        print(f"   ✅ {len(aplicaciones_data)} aplicaciones creadas con sus líderes técnicos")
        
        # ===== CREAR CREDENCIALES DE EJEMPLO =====
        print("🔐 Creando credenciales de ejemplo...")
        
        credenciales = [
            {
                'nombre_servidor': 'COM-SYN-PRO-VMA-O11-001',
                'ip': '10.164.113.160',
                'descripcion': 'Synergia - Producción',
                'tipo_autenticacion': 'password',
                'usuario': 'root',
                'contrasena': 'Synergia2024'
            },
            {
                'nombre_servidor': 'COM-RDD-PRO-VMA-O11-002',
                'ip': '10.164.113.161',
                'descripcion': 'RDD - Producción',
                'tipo_autenticacion': 'password',
                'usuario': 'admin',
                'contrasena': 'RDD2024'
            },
            {
                'nombre_servidor': 'COM-SFR-PRO-VMA-O11-003',
                'ip': '10.164.113.162',
                'descripcion': 'Salesforce - Producción',
                'tipo_autenticacion': 'llave',
                'usuario': 'sfadmin',
                'llave_privada': '-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----'
            }
        ]
        
        for cred_data in credenciales:
            # Identificar aplicación automáticamente
            nombre_upper = cred_data['nombre_servidor'].upper()
            aplicacion = None
            for app_item in aplicaciones_data:
                if app_item['codigo'] in nombre_upper:
                    aplicacion = Aplicacion.query.filter_by(codigo=app_item['codigo']).first()
                    break
            
            nueva_cred = Credencial(
                nombre_servidor=cred_data['nombre_servidor'],
                ip=cred_data['ip'],
                descripcion=cred_data['descripcion'],
                tipo_autenticacion=cred_data['tipo_autenticacion'],
                usuario=cred_data['usuario'],
                usuario_id=admin.id,
                aplicacion_id=aplicacion.id if aplicacion else None
            )
            
            if cred_data['tipo_autenticacion'] == 'password':
                nueva_cred.set_contrasena(cred_data['contrasena'])
            else:
                nueva_cred.llave_privada = cred_data.get('llave_privada', '')
            
            db.session.add(nueva_cred)
        
        db.session.commit()
        print(f"   ✅ {len(credenciales)} credenciales creadas")
        
        print("\n" + "="*50)
        print("✅ BASE DE DATOS CREADA CON DATOS DE PRUEBA")
        print("="*50)
        print("📧 Usuario: admin@gestor.com")
        print("🔑 Contraseña: admin123")
        print(f"📱 Aplicaciones: {len(aplicaciones_data)}")
        print(f"👥 Líderes: {len(aplicaciones_data) * 2} (1 principal + 1 alterno por aplicación)")
        print(f"🔐 Credenciales: {len(credenciales)}")
        print("="*50)

if __name__ == '__main__':
    seed()