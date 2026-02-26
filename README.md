
**ASCDROP** es una aplicación web segura para transferencia de archivos desarrollada por **ASCITGROUP**. 
🔒 Plataforma web profesional para transferencia segura de archivos con auditoría completa.

## ✨ Características

- 🔐 **Autenticación segura** (usuarios: amatique/admin, Gerencia/admin, Invitado/root)
- 📤 **Subida múltiple** de archivos y carpetas (ZIP automático)
- 📥 **Descarga segura** con logs
- 🗑️ **Eliminación auditada** con confirmación
- 📊 **Sistema de logs** rotativos (solo admin)
- 🎨 **Branding profesional** ASCITGROUP
- 📱 **Responsive** y moderno UI


##📊 Logs
Accede en /logserver (solo amatique). Los logs rotan automáticamente a 5MB.

🔧 Personalización
Cambiar usuarios: Edita USERS en app.py

Logo: Reemplaza static/logo.png

Colores: Modifica los gradientes CSS en las plantillas

📄 Licencia
MIT License - © 2026 ASCITGROUP - Marcos Hernández


[![LinkedIn - Marcos Hernández](https://img.shields.io/badge/LinkedIn-Marcos%20Hern%C3%A1ndez-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marcosh1488/)

## 🚀 Instalación rápida
```bash
# Clonar repositorio
git clone https://github.com/tuusuario/ASCDROP.git
cd ASCDROP

# Instalar dependencias
pip install -r requirements.txt

# Crear carpeta static para logo
mkdir static
# Copiar tu logo como static/logo.png
Esta configuracion es (opcional)
__________________________

# Ejecutar
python ascdrop.py 

🌐 Accede en: http://IP:5000

| Usuario       | Contraseña | Permisos Logs |
| --------      | ---------- | ------------- |
| Administrador | admin      | ✅ Admin       |
| Gerencia      | admin      | ❌ Usuario     |
| Invitado      | root       | ❌ Usuario     |
