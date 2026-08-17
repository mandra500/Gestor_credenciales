// ===== FUNCIONES PARA EDICIÓN =====
console.log('✅ Scripts de edición cargados');

// ===== MOSTRAR CONTRASEÑA EN EDICIÓN =====
function verPasswordEditar(id) {
    const display = document.getElementById('passwordDisplay');
    
    if (display.textContent === '••••••••') {
        fetch('/obtener-contrasena/' + id)
            .then(response => response.json())
            .then(data => {
                if (data.contrasena) {
                    display.textContent = data.contrasena;
                    mostrarNotificacion('👁️ Contraseña visible por 10 segundos');
                    setTimeout(() => {
                        display.textContent = '••••••••';
                    }, 10000);
                } else {
                    if (data.sugerencia) {
                        mostrarNotificacion('⚠️ ' + data.error + ' - ' + data.sugerencia);
                    } else {
                        mostrarNotificacion('⚠️ ' + (data.error || 'No se pudo obtener la contraseña'));
                    }
                }
            })
            .catch(error => {
                mostrarNotificacion('❌ Error al obtener la contraseña');
            });
    } else {
        display.textContent = '••••••••';
        mostrarNotificacion('🔒 Contraseña oculta');
    }
}

// ===== COPIAR CONTRASEÑA EN EDICIÓN =====
function copiarPasswordEditar(id) {
    const display = document.getElementById('passwordDisplay');
    const textoACopiar = display.textContent;
    
    console.log('📋 Intentando copiar:', textoACopiar);
    
    if (textoACopiar === '••••••••') {
        fetch('/obtener-contrasena/' + id)
            .then(response => response.json())
            .then(data => {
                if (data.contrasena) {
                    copiarAlPortapapeles(data.contrasena);
                } else {
                    mostrarNotificacion('⚠️ ' + (data.error || 'No se pudo obtener la contraseña'));
                }
            })
            .catch(error => {
                mostrarNotificacion('❌ Error al obtener la contraseña');
            });
    } else {
        copiarAlPortapapeles(textoACopiar);
    }
}

// ===== FUNCIÓN PARA COPIAR AL PORTAPAPELES =====
function copiarAlPortapapeles(texto) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto)
            .then(() => {
                console.log('✅ Copiado:', texto);
                mostrarNotificacion('✅ Contraseña copiada al portapapeles');
            })
            .catch(() => {
                copiarFallbackEditar(texto);
            });
    } else {
        copiarFallbackEditar(texto);
    }
}

// ===== COPIAR CON FALLBACK =====
function copiarFallbackEditar(texto) {
    try {
        const textarea = document.createElement('textarea');
        textarea.value = texto;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        textarea.style.top = '0';
        textarea.style.left = '0';
        textarea.style.width = '1px';
        textarea.style.height = '1px';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        mostrarNotificacion('✅ Contraseña copiada al portapapeles');
    } catch (e) {
        mostrarNotificacion('❌ No se pudo copiar');
    }
}

// ===== MOSTRAR NOMBRE DE ARCHIVO =====
function mostrarNombreArchivo() {
    const input = document.getElementById('fileInput');
    const nombreDiv = document.getElementById('nombreArchivo');
    if (input.files && input.files[0]) {
        nombreDiv.innerHTML = '✅ Archivo seleccionado: <strong>' + input.files[0].name + '</strong> (' + (input.files[0].size / 1024).toFixed(1) + ' KB)';
    } else {
        nombreDiv.innerHTML = '';
    }
}

// ===== NOTIFICACIÓN =====
function mostrarNotificacion(mensaje) {
    const existing = document.querySelector('.custom-notification');
    if (existing) existing.remove();
    
    const notificacion = document.createElement('div');
    notificacion.className = 'custom-notification';
    notificacion.textContent = mensaje;
    notificacion.style.cssText = `
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        background: var(--color-primary, #D4A373);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 8px 30px rgba(212, 163, 115, 0.4);
        z-index: 9999;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        max-width: 90%;
        text-align: center;
        animation: fadeInUp 0.3s ease;
    `;
    document.body.appendChild(notificacion);
    
    setTimeout(() => {
        notificacion.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        notificacion.style.opacity = '0';
        notificacion.style.transform = 'translateX(-50%) translateY(20px)';
        setTimeout(() => {
            if (notificacion.parentNode) {
                document.body.removeChild(notificacion);
            }
        }, 300);
    }, 3000);
}

// ===== ESTILO =====
const styleNotifEditar = document.createElement('style');
styleNotifEditar.textContent = `
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateX(-50%) translateY(20px); }
        to { opacity: 1; transform: translateX(-50%) translateY(0); }
    }
`;
document.head.appendChild(styleNotifEditar);