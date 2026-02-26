
**ASCDROP** es una aplicación web segura para transferencia de archivos desarrollada por **ASCITGROUP**. 
🔒 Plataforma web profesional para transferencia segura de archivos con auditoría completa.

<img width="1275" height="556" alt="image" src="https://github.com/user-attachments/assets/60daef82-a9a3-4b13-abb8-4f1ba330f7a4" />


## ✨ Características

- 🔐 **Autenticación segura** (usuarios: Administrador/admin, Gerencia/root, Invitado/Admin123)
- 📤 **Subida múltiple** de archivos y carpetas (ZIP automático)
- 📥 **Descarga segura** con logs
- 🗑️ **Eliminación auditada** con confirmación
- 📊 **Sistema de logs** rotativos (solo admin)
- 🎨 **Branding profesional** ASCITGROUP
- 📱 **Responsive** y moderno UI

<img width="1361" height="588" alt="image" src="https://github.com/user-attachments/assets/65bda836-0ff2-41b5-89db-b823d62b8492" />



##📊 Logs
Accede en /logserver (solo el usuario Administrador). Los logs rotan automáticamente a 10MB. (se puede cambiar segun a preferencia)

<img width="1248" height="253" alt="image" src="https://github.com/user-attachments/assets/5697f410-f4f7-4fe4-8aee-f2b7cba717fc" />


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
