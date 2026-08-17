# jira_mock.py
"""
Simulador de JIRA para pruebas - Tickets con formato realista
"""

from datetime import datetime, timedelta
import json

class JiraMock:
    """Simulador de JIRA para pruebas"""
    
    def __init__(self):
        # Proyectos simulados
        self.projects = [
            {
                "id": 1,
                "key": "PROY",
                "name": "Proyecto Principal",
                "lead": "Admin",
                "status": "active"
            },
            {
                "id": 2,
                "key": "REQ",
                "name": "Requerimientos",
                "lead": "Product Owner",
                "status": "active"
            },
            {
                "id": 3,
                "key": "TGR",
                "name": "Tareas Generales",
                "lead": "Project Manager",
                "status": "active"
            },
            {
                "id": 4,
                "key": "TEST",
                "name": "Proyecto de Pruebas",
                "lead": "Tester",
                "status": "active"
            }
        ]
        
        # ===== INCIDENCIAS SIMULADAS (CON FORMATO REALISTA) =====
        self.issues = [
            # ===== TICKETS REQ (Requerimientos) =====
            {
                "id": 1,
                "key": "REQ-336",
                "summary": "Implementar autenticación con JWT en el Gestor de Credenciales",
                "description": "Se necesita implementar autenticación JWT para mejorar la seguridad del sistema",
                "status": "Open",
                "priority": "High",
                "assignee": "Admin",
                "created": (datetime.now() - timedelta(days=5)).isoformat(),
                "updated": (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                "id": 2,
                "key": "REQ-337",
                "summary": "Integración con JIRA para check-in de credenciales",
                "description": "Permitir que los usuarios hagan check-in de credenciales asociadas a tickets de JIRA",
                "status": "In Progress",
                "priority": "High",
                "assignee": "Developer",
                "created": (datetime.now() - timedelta(days=3)).isoformat(),
                "updated": datetime.now().isoformat()
            },
            {
                "id": 3,
                "key": "REQ-338",
                "summary": "Dashboard para visualización de credenciales por aplicación",
                "description": "Crear un dashboard interactivo que muestre estadísticas de credenciales",
                "status": "Open",
                "priority": "Medium",
                "assignee": "Developer",
                "created": (datetime.now() - timedelta(days=1)).isoformat(),
                "updated": datetime.now().isoformat()
            },
            
            # ===== TICKETS TGR (Tareas Generales) =====
            {
                "id": 4,
                "key": "TGR-1837",
                "summary": "Actualizar documentación del API de credenciales",
                "description": "La documentación del API necesita actualizarse con los nuevos endpoints",
                "status": "Open",
                "priority": "Medium",
                "assignee": "Admin",
                "created": (datetime.now() - timedelta(days=7)).isoformat(),
                "updated": (datetime.now() - timedelta(days=3)).isoformat()
            },
            {
                "id": 5,
                "key": "TGR-1838",
                "summary": "Implementar backup automático de la base de datos",
                "description": "Crear un sistema de backups programados para la BD de credenciales",
                "status": "In Progress",
                "priority": "High",
                "assignee": "Developer",
                "created": (datetime.now() - timedelta(days=2)).isoformat(),
                "updated": datetime.now().isoformat()
            },
            {
                "id": 6,
                "key": "TGR-1839",
                "summary": "Configurar monitoreo de sesiones activas",
                "description": "Implementar sistema que detecte sesiones de credenciales activas",
                "status": "Open",
                "priority": "Low",
                "assignee": "Admin",
                "created": (datetime.now() - timedelta(days=1)).isoformat(),
                "updated": datetime.now().isoformat()
            },
            
            # ===== TICKETS PROY (Proyecto Principal) =====
            {
                "id": 7,
                "key": "PROY-1",
                "summary": "Crear credencial para servidor CRS-JUMP-PRO-VM-011-001",
                "description": "Configurar acceso SSH para el servidor de producción",
                "status": "Open",
                "priority": "Critical",
                "assignee": "Admin",
                "created": (datetime.now() - timedelta(days=10)).isoformat(),
                "updated": (datetime.now() - timedelta(days=5)).isoformat()
            },
            {
                "id": 8,
                "key": "PROY-2",
                "summary": "Configurar credenciales para base de datos PostgreSQL",
                "description": "Crear usuario y contraseña para acceso a la base de datos",
                "status": "Open",
                "priority": "High",
                "assignee": "Developer",
                "created": (datetime.now() - timedelta(days=3)).isoformat(),
                "updated": datetime.now().isoformat()
            },
            
            # ===== TICKETS TEST (Pruebas) =====
            {
                "id": 9,
                "key": "TEST-1",
                "summary": "Pruebas de integración del sistema de credenciales",
                "description": "Realizar pruebas de integración de todos los módulos",
                "status": "Open",
                "priority": "Medium",
                "assignee": "Tester",
                "created": (datetime.now() - timedelta(days=2)).isoformat(),
                "updated": datetime.now().isoformat()
            }
        ]
        
        self.issues_counter = 10
        self.comments_counter = 10

    # ===== MÉTODOS PRINCIPALES =====
    
    def get_projects(self):
        return self.projects
    
    def get_project(self, project_key):
        for project in self.projects:
            if project["key"] == project_key:
                return project
        return None
    
    def create_issue(self, project_key, summary, description=None, priority="Medium", assignee=None):
        project = self.get_project(project_key)
        if not project:
            return {"error": f"Proyecto {project_key} no encontrado", "status": "error"}
        
        new_issue = {
            "id": self.issues_counter,
            "key": f"{project_key}-{self.issues_counter}",
            "summary": summary,
            "description": description or "",
            "status": "Open",
            "priority": priority,
            "assignee": assignee or "Unassigned",
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        
        self.issues_counter += 1
        self.issues.append(new_issue)
        
        return {
            "id": new_issue["id"],
            "key": new_issue["key"],
            "status": "created",
            "url": f"https://mock-jira.local/browse/{new_issue['key']}"
        }
    
    def get_issue(self, issue_key):
        for issue in self.issues:
            if issue["key"] == issue_key:
                return issue
        return None
    
    def update_issue(self, issue_key, status=None, summary=None, assignee=None, priority=None):
        issue = self.get_issue(issue_key)
        if not issue:
            return {"error": f"Incidencia {issue_key} no encontrada", "status": "error"}
        
        if status:
            issue["status"] = status
        if summary:
            issue["summary"] = summary
        if assignee:
            issue["assignee"] = assignee
        if priority:
            issue["priority"] = priority
        
        issue["updated"] = datetime.now().isoformat()
        return {"key": issue_key, "status": "updated", "updated_at": issue["updated"]}
    
    def get_issues_by_project(self, project_key):
        return [issue for issue in self.issues if issue["key"].startswith(project_key)]
    
    def add_comment(self, issue_key, comment):
        self.comments_counter += 1
        return {
            "id": self.comments_counter,
            "body": comment,
            "author": "Gestor Credenciales",
            "created": datetime.now().isoformat()
        }


# ===== INSTANCIA GLOBAL =====
_jira_mock_instance = None

def get_jira_mock():
    global _jira_mock_instance
    if _jira_mock_instance is None:
        _jira_mock_instance = JiraMock()
    return _jira_mock_instance


# ===== FUNCIONES DE INTERFAZ =====

def obtener_jira_client():
    return {'url': 'https://mock-jira.local', 'auth': None, 'headers': {}}

def is_jira_enabled():
    return True

def get_jira_config():
    import os
    return {
        'url': os.environ.get('JIRA_URL', 'https://mock-jira.local'),
        'email': os.environ.get('JIRA_EMAIL', 'admin@gestor.com'),
        'api_token': os.environ.get('JIRA_API_TOKEN', 'mock-token'),
        'project_key': os.environ.get('JIRA_PROJECT_KEY', 'PROY'),
        'enabled': os.environ.get('JIRA_ENABLED', 'true').lower() == 'true'
    }

def print_jira_mock_info():
    mock = get_jira_mock()
    print("\n" + "="*60)
    print("🔧 JIRA MOCK ACTIVADO - EN MODO PRUEBAS")
    print("="*60)
    
    print("\n📋 Proyectos disponibles:")
    for p in mock.projects:
        print(f"   - {p['key']}: {p['name']}")
    
    print("\n📋 Tickets disponibles para prueba:")
    print("   " + "-"*40)
    for i in mock.issues:
        print(f"   {i['key']}: {i['summary'][:50]}... ({i['status']})")
    print("="*60 + "\n")

def reset_jira_mock():
    global _jira_mock_instance
    _jira_mock_instance = JiraMock()
    print("🔄 JIRA Mock reiniciado")


# ===== FUNCIONES DE COMPATIBILIDAD =====

def create_ticket(project_key, summary, description=None, priority="Medium", assignee=None):
    mock = get_jira_mock()
    return mock.create_issue(project_key, summary, description, priority, assignee)

def get_ticket(ticket_key):
    mock = get_jira_mock()
    return mock.get_issue(ticket_key)

def update_ticket(ticket_key, **kwargs):
    mock = get_jira_mock()
    return mock.update_issue(ticket_key, **kwargs)

def get_tickets_by_project(project_key):
    mock = get_jira_mock()
    return mock.get_issues_by_project(project_key)

def add_comment_to_ticket(ticket_key, comment):
    mock = get_jira_mock()
    return mock.add_comment(ticket_key, comment)

def buscar_ticket_jira(numero_ticket):
    """Busca un ticket en Jira (Mock) - Formato: PROY-123"""
    mock = get_jira_mock()
    
    # Verificar que el ticket existe
    issue = mock.get_issue(numero_ticket)
    
    if issue:
        return {
            'id': issue['id'],
            'key': issue['key'],
            'summary': issue['summary'],
            'status': issue['status'],
            'assignee': issue.get('assignee'),
            'priority': issue.get('priority'),
            'created': issue['created'],
            'updated': issue['updated'],
            'description': issue.get('description', ''),
            'url': f"https://mock-jira.local/browse/{issue['key']}"
        }
    
    print(f"⚠️ Ticket {numero_ticket} no encontrado en el mock")
    return None

def actualizar_ticket_jira(ticket_key, status=None, comentario=None):
    """Actualiza un ticket en Jira (Mock)"""
    mock = get_jira_mock()
    
    issue = mock.get_issue(ticket_key)
    if not issue:
        print(f"⚠️ Ticket {ticket_key} no encontrado para actualizar")
        return False
    
    if status:
        mock.update_issue(ticket_key, status=status)
        print(f"✅ Ticket {ticket_key} actualizado a estado: {status}")
    
    if comentario:
        mock.add_comment(ticket_key, comentario)
        print(f"✅ Comentario agregado al ticket {ticket_key}")
    
    return True


if __name__ == "__main__":
    print_jira_mock_info()