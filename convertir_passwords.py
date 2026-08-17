"""Script para convertir contraseñas de hash a encriptación AES"""
from app import app, db
from database import Credencial, encriptar_contrasena
import bcrypt

def convertir_contraseñas():
    with app.app_context():
        # Obtener todas las credenciales con contraseña
        credenciales = Credencial.query.filter(
            Credencial.tipo_autenticacion == 'password',
            Credencial.contrasena.isnot(None)
        ).all()
        
        if not credenciales:
            print("📭 No hay contraseñas para convertir")
            return
        
        print(f"🔑 Convirtiendo {len(credenciales)} contraseñas...")
        print("\n⚠️  IMPORTANTE: Necesitas saber la contraseña original para convertirla.")
        print("   Como las contraseñas están hasheadas, no se pueden recuperar.\n")
        
        for cred in credenciales:
            print(f"📌 {cred.nombre_servidor} (ID: {cred.id})")
            print(f"   Usuario: {cred.usuario}")
            print(f"   IP: {cred.ip}")
            
            # Preguntar si quiere convertir manualmente
            respuesta = input("   ¿Quieres restablecer esta contraseña? (s/n): ").lower()
            
            if respuesta == 's':
                nueva_pass = input("   Ingresa la nueva contraseña: ")
                if nueva_pass:
                    # Encriptar con AES
                    cred.contrasena = encriptar_contrasena(nueva_pass)
                    print(f"   ✅ Contraseña restablecida y encriptada para {cred.nombre_servidor}\n")
                else:
                    print("   ⏭️  Contraseña no cambiada\n")
            else:
                print("   ⏭️  Saltando...\n")
        
        db.session.commit()
        print("\n✅ Proceso completado. Las contraseñas convertidas ahora son recuperables.")

if __name__ == '__main__':
    convertir_contraseñas()