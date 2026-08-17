// ===== SIDEBAR - ESTADO Y FUNCIONES =====
let sidebarVisible = true;

// ===== CARGAR ESTADO GUARDADO =====
function loadSidebarState() {
    const saved = localStorage.getItem('sidebarVisible');
    if (saved !== null) {
        sidebarVisible = saved === 'true';
    } else {
        sidebarVisible = window.innerWidth > 768;
    }
    applySidebarState();
}

// ===== APLICAR ESTADO =====
function applySidebarState() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const hamburgerIcon = document.querySelector('.hamburger-icon');
    const overlay = document.getElementById('sidebarOverlay');

    if (!sidebarVisible) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        if (hamburgerIcon) hamburgerIcon.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
    } else {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('expanded');
        if (hamburgerIcon) hamburgerIcon.classList.add('open');
        if (overlay && window.innerWidth <= 768) overlay.classList.add('active');
    }
}

// ===== TOGGLE SIDEBAR =====
function toggleSidebar() {
    sidebarVisible = !sidebarVisible;
    localStorage.setItem('sidebarVisible', sidebarVisible);
    applySidebarState();
}

// ===== TOGGLE SUBMENÚ =====
function toggleSubmenu(id) {
    const submenu = document.getElementById(id);
    const arrow = document.getElementById('arrow' + id.replace('submenu', ''));
    submenu.classList.toggle('open');
    if (arrow) arrow.classList.toggle('open');
}

// ===== FILTRO (DEMO) =====
function filtrarPor(categoria) {
    alert('🔍 Filtro por: ' + categoria + '\n(En la versión final, esto mostrará solo las credenciales de esta categoría)');
}

// ===== CERRAR SIDEBAR EN MÓVIL AL NAVEGAR =====
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sidebar-menu a:not(.menu-toggle)').forEach(link => {
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 && !this.classList.contains('menu-toggle')) {
                sidebarVisible = false;
                localStorage.setItem('sidebarVisible', false);
                applySidebarState();
            }
        });
    });

    // ===== MANEJAR CAMBIO DE TAMAÑO =====
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            loadSidebarState();
        } else {
            const saved = localStorage.getItem('sidebarVisible');
            if (saved === null || saved === 'true') {
                sidebarVisible = false;
                localStorage.setItem('sidebarVisible', false);
                applySidebarState();
            }
        }
    });

    // ===== INICIALIZAR =====
    loadSidebarState();

    // Abrir submenús si hay un enlace activo dentro
    document.querySelectorAll('.submenu').forEach(sub => {
        if (sub.querySelector('.active')) {
            sub.classList.add('open');
            const arrow = document.getElementById('arrow' + sub.id.replace('submenu', ''));
            if (arrow) arrow.classList.add('open');
        }
    });

    // En móvil, ocultar sidebar al cargar
    if (window.innerWidth <= 768) {
        sidebarVisible = false;
        localStorage.setItem('sidebarVisible', false);
        applySidebarState();
    }
});