// ===== FUNCIONES PARA CREDENCIALES (Dashboard) =====
console.log('✅ Scripts de credenciales cargados');

// ===== VER CONTRASEÑA =====
function verPassword(id) {
    console.log('🔍 Ver contraseña para ID:', id);
    const span = document.getElementById('password_' + id);
    
    if (!span) {
        mostrarNotificacion('❌ Error al encontrar la contraseña');
        return;
    }
    
    const btn = span.parentElement.querySelector('button:first-of-type');
    
    if (span.textContent === '••••••••') {
        console.log('📤 Solicitando contraseña al servidor...');
        
        fetch('/obtener-contrasena/' + id)
            .then(response => {
                console.log('📥 Respuesta recibida, status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('📦 Datos recibidos:', data);
                if (data.contrasena) {
                    span.textContent = data.contrasena;
                    if (btn) btn.textContent = '🙈';
                    mostrarNotificacion('👁️ Contraseña visible por 10 segundos');
                    setTimeout(() => {
                        span.textContent = '••••••••';
                        if (btn) btn.textContent = '👁️';
                    }, 10000);
                } else {
                    console.error('❌ Error en datos:', data.error);
                    if (data.sugerencia) {
                        mostrarNotificacion('⚠️ ' + data.error + ' - ' + data.sugerencia);
                        setTimeout(() => {
                            window.location.href = '/editar/' + id;
                        }, 3000);
                    } else {
                        mostrarNotificacion('⚠️ ' + (data.error || 'No se pudo obtener la contraseña'));
                    }
                }
            })
            .catch(error => {
                console.error('❌ Error en fetch:', error);
                mostrarNotificacion('❌ Error al obtener la contraseña');
            });
    } else {
        span.textContent = '••••••••';
        if (btn) btn.textContent = '👁️';
        mostrarNotificacion('🔒 Contraseña oculta');
    }
}

// ===== COPIAR CONTRASEÑA =====
function copiarPassword(id) {
    console.log('📋 Copiar contraseña para ID:', id);
    const span = document.getElementById('password_' + id);
    
    if (!span) {
        mostrarNotificacion('❌ Error al encontrar la contraseña');
        return;
    }
    
    const copiar = (texto) => {
        console.log('📝 Copiando texto...');
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(texto)
                .then(() => {
                    console.log('✅ Copiado exitosamente');
                    mostrarNotificacion('✅ Contraseña copiada al portapapeles');
                })
                .catch((err) => {
                    console.warn('⚠️ Clipboard falló, usando fallback:', err);
                    copiarFallback(texto);
                });
        } else {
            console.warn('⚠️ Clipboard no disponible, usando fallback');
            copiarFallback(texto);
        }
    };
    
    if (span.textContent === '••••••••') {
        console.log('📤 Solicitando contraseña para copiar...');
        fetch('/obtener-contrasena/' + id)
            .then(response => {
                console.log('📥 Respuesta recibida, status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('📦 Datos recibidos:', data);
                if (data.contrasena) {
                    copiar(data.contrasena);
                } else {
                    console.error('❌ Error en datos:', data.error);
                    if (data.sugerencia) {
                        mostrarNotificacion('⚠️ ' + data.error + ' - ' + data.sugerencia);
                        setTimeout(() => {
                            window.location.href = '/editar/' + id;
                        }, 3000);
                    } else {
                        mostrarNotificacion('⚠️ ' + (data.error || 'No se pudo obtener la contraseña'));
                    }
                }
            })
            .catch(error => {
                console.error('❌ Error en fetch:', error);
                mostrarNotificacion('❌ Error al obtener la contraseña');
            });
    } else {
        copiar(span.textContent);
    }
}

// ===== COPIAR CON FALLBACK =====
function copiarFallback(texto) {
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
        const success = document.execCommand('copy');
        document.body.removeChild(textarea);
        if (success) {
            console.log('✅ Copiado exitosamente con fallback');
            mostrarNotificacion('✅ Contraseña copiada al portapapeles');
        } else {
            console.error('❌ Fallback también falló');
            mostrarNotificacion('❌ No se pudo copiar');
        }
    } catch (e) {
        console.error('❌ Error en copiarFallback:', e);
        mostrarNotificacion('❌ No se pudo copiar');
    }
}

// ===== COPIAR TEXTO (IP) =====
function copiarTexto(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
        mostrarNotificacion('❌ No se encontró el elemento');
        return;
    }
    const texto = element.textContent.trim();
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto)
            .then(() => mostrarNotificacion('✅ IP copiada al portapapeles'))
            .catch(() => copiarFallbackSimple(texto, 'IP'));
    } else {
        copiarFallbackSimple(texto, 'IP');
    }
}

// ===== COPIAR USUARIO =====
function copiarTextoUsuario(usuario) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(usuario)
            .then(() => mostrarNotificacion('✅ Usuario copiado al portapapeles'))
            .catch(() => copiarFallbackSimple(usuario, 'Usuario'));
    } else {
        copiarFallbackSimple(usuario, 'Usuario');
    }
}

// ===== COPIAR FALLBACK SIMPLE =====
function copiarFallbackSimple(texto, tipo) {
    try {
        const textarea = document.createElement('textarea');
        textarea.value = texto;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        textarea.style.top = '0';
        textarea.style.left = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        mostrarNotificacion('✅ ' + tipo + ' copiado al portapapeles');
    } catch (e) {
        mostrarNotificacion('❌ No se pudo copiar');
    }
}

// ===== NOTIFICACIÓN TEMPORAL =====
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

// ===== ESTILO PARA LA NOTIFICACIÓN =====
const styleNotif = document.createElement('style');
styleNotif.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
`;
document.head.appendChild(styleNotif);

console.log('✅ Scripts de credenciales cargados correctamente');