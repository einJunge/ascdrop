import os
import io
import zipfile
import secrets
from datetime import datetime
from flask import Flask, request, redirect, render_template_string, session, send_from_directory, abort, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

UPLOAD_FOLDER = "storage"
LOG_FILE = "activity.log"
MAX_LOG_SIZE_MB = 5

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERS = {
    "Administrador": "admin",
    "Gerencia": "admin123",
    "Invitado": "root"
}

# ================= TEMPLATES =================

LOGIN_HTML = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>ASCDROP - ASCITGROUP</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%);
            color:#e5e7eb;
            display:flex;
            align-items:center;
            justify-content:center;
            min-height:100vh;
            overflow:auto;
        }
        .logo {
            width:140px;
            height:auto;
            margin-bottom:20px;
            display:block;
            margin-left:auto;
            margin-right:auto;
        }
        .box {
            background:rgba(17,24,39,0.95);
            backdrop-filter:blur(20px);
            padding:40px 30px;
            border-radius:16px;
            box-shadow:0 20px 40px rgba(0,0,0,0.6);
            width:100%;
            max-width:360px;
            border:1px solid rgba(59,130,246,0.3);
        }
        h2 { 
            margin-bottom:30px; 
            color:#fff; 
            text-align:center;
            font-weight:600;
            font-size:24px;
            letter-spacing:-0.5px;
        }
        .subtitle {
            text-align:center;
            color:#9ca3af;
            font-size:14px;
            margin-bottom:25px;
        }
        label { 
            display:block; 
            margin-bottom:8px; 
            font-size:14px; 
            color:#d1d5db; 
            font-weight:500;
        }
        input {
            width:100%;
            padding:12px 16px;
            margin-bottom:20px;
            border-radius:10px;
            border:1px solid #374151;
            background:rgba(15,23,42,0.8);
            color:#e5e7eb;
            font-size:15px;
            transition:all 0.2s;
        }
        input:focus {
            outline:none;
            border-color:#3b82f6;
            box-shadow:0 0 0 3px rgba(59,130,246,0.1);
        }
        button {
            width:100%;
            padding:12px;
            border:none;
            border-radius:10px;
            cursor:pointer;
            font-weight:600;
            font-size:15px;
            background:linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color:#022c22;
            transition:all 0.2s;
        }
        button:hover {
            transform:translateY(-1px);
            box-shadow:0 10px 20px rgba(34,197,94,0.3);
        }
        .footer {
            text-align:center;
            margin-top:25px;
            font-size:12px;
            color:#6b7280;
        }
        .creator {
            margin-top:15px;
            font-size:13px;
            color:#9ca3af;
        }
        .creator a {
            color:#3b82f6;
            text-decoration:none;
        }
    </style>
</head>
<body>
    <div class="box">
        <img src="/static/logo.png" alt="ASCITGROUP" class="logo">
        <h2>ASCDROP</h2>
        <div class="subtitle">Transferencia segura de archivos</div>
        <form method="POST">
            <label for="username">Usuario</label>
            <input type="text" name="username" id="username" required>

            <label for="password">Contraseña</label>
            <input type="password" name="password" id="password" required>

            <button type="submit">Acceder al nodo</button>
        </form>
        <div class="footer">
            <div>ASCITGROUP</div>
            <div>Protegiendo su infraestructura IT</div>
        </div>
        <div class="creator">
            Creado por <a href="https://www.linkedin.com/in/marcosh1488/" target="_blank">Marcos Hernández</a>
        </div>
    </div>
</body>
</html>
"""

PANEL_HTML = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>ASCDROP - ASCITGROUP</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%);
            color:#e5e7eb;
            margin:0;
            padding:20px;
            min-height:100vh;
        }
        .header {
            display:flex;
            align-items:center;
            justify-content:space-between;
            margin-bottom:30px;
            padding-bottom:20px;
            border-bottom:1px solid rgba(59,130,246,0.3);
        }
        .logo {
            width:120px;
            height:auto;
        }
        .title {
            font-size:28px;
            font-weight:700;
            background:linear-gradient(135deg, #3b82f6 0%, #22c55e 100%);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            background-clip:text;
        }
        .topbar {
            display:flex;
            gap:20px;
            font-size:14px;
        }
        .topbar a {
            color:#60a5fa;
            text-decoration:none;
            font-weight:500;
        }
        .topbar a:hover {
            color:#3b82f6;
        }
        .upload-section {
            background:rgba(17,24,39,0.8);
            backdrop-filter:blur(10px);
            padding:25px;
            border-radius:16px;
            margin-bottom:30px;
            border:1px solid rgba(59,130,246,0.2);
        }
        .upload-section h3 {
            color:#fff;
            margin-bottom:20px;
            font-weight:600;
            font-size:18px;
        }
        .upload-grid {
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:20px;
            margin-bottom:20px;
        }
        input[type="file"] {
            width:100%;
            padding:12px;
            border-radius:10px;
            border:1px solid #374151;
            background:rgba(15,23,42,0.8);
            color:#e5e7eb;
        }
        .btn-upload {
            background:linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color:#eff6ff;
            border:none;
            padding:12px 24px;
            border-radius:10px;
            font-weight:600;
            font-size:14px;
            cursor:pointer;
            transition:all 0.2s;
        }
        .btn-upload:hover {
            transform:translateY(-1px);
            box-shadow:0 10px 25px rgba(59,130,246,0.4);
        }

        table {
            width:100%;
            border-collapse:collapse;
            background:rgba(17,24,39,0.8);
            backdrop-filter:blur(10px);
            border-radius:16px;
            overflow:hidden;
            border:1px solid rgba(59,130,246,0.2);
            font-size:15px;
        }
        th {
            background:linear-gradient(135deg, #1e293b 0%, #334155 100%);
            text-align:left;
            padding:18px 20px;
            font-weight:600;
            color:#f1f5f9;
        }
        td {
            padding:16px 20px;
            border-bottom:1px solid rgba(71,85,105,0.3);
        }
        tr:hover td {
            background:rgba(59,130,246,0.1);
        }
        .btn-download,
        .btn-delete {
            padding:8px 16px;
            border-radius:8px;
            border:none;
            font-size:13px;
            font-weight:600;
            cursor:pointer;
            transition:all 0.2s;
            text-decoration:none;
            display:inline-block;
        }
        .btn-download {
            background:linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color:#eff6ff;
            margin-right:8px;
        }
        .btn-download:hover {
            transform:translateY(-1px);
            box-shadow:0 5px 15px rgba(59,130,246,0.4);
        }
        .btn-delete {
            background:linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color:#fef2f2;
        }
        .btn-delete:hover {
            transform:translateY(-1px);
            box-shadow:0 5px 15px rgba(239,68,68,0.4);
        }
        .footer {
            text-align:center;
            margin-top:40px;
            padding-top:30px;
            border-top:1px solid rgba(59,130,246,0.3);
            font-size:13px;
            color:#6b7280;
        }
        @media (max-width:768px) {
            .upload-grid { grid-template-columns:1fr; }
            .header { flex-direction:column; gap:15px; text-align:center; }
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/logo.png" alt="ASCITGROUP" class="logo">
        <div>
            <div class="title">ASCDROP</div>
        </div>
        <div class="topbar">
            <a href="/logserver">📊 Logs</a>
            <a href="/logout">🚪 Cerrar sesión</a>
        </div>
    </div>

    <div class="upload-section">
        <h3>📤 Transferir archivos al nodo</h3>
        <div class="upload-grid">
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <strong>Archivos individuales</strong><br>
                <input type="file" name="files" multiple>
                <button type="submit" class="btn-upload">Subir</button>
            </form>

            <form action="/upload_folder" method="POST" enctype="multipart/form-data">
                <strong>Carpeta completa (ZIP)</strong><br>
                <input type="file" name="folder" webkitdirectory directory multiple>
                <button type="submit" class="btn-upload">Comprimir y subir</button>
            </form>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>📄 Archivo</th>
                <th>🔐 Acciones</th>
            </tr>
        </thead>
        <tbody>
        {% for file in files %}
            <tr>
                <td style="font-family:monospace;">{{ file }}</td>
                <td>
                    <a href="/download/{{ file }}" class="btn-download">📥 Descargar</a>
                    <form action="/delete/{{ file }}" method="POST" style="display:inline;">
                        <button type="submit" class="btn-delete" onclick="return confirm('¿Eliminar {{ file }}?')">🗑️ Borrar</button>
                    </form>
                </td>
            </tr>
        {% endfor %}
        </tbody>
    </table>

    <div class="footer">
        <strong>ASCITGROUP</strong><br>
        Protegiendo su infraestructura IT<br>
        <small>Creado por Marcos Hernández | <a href="https://www.linkedin.com/in/marcosh1488/" target="_blank" style="color:#60a5fa;">LinkedIn</a></small>
    </div>
</body>
</html>
"""

# ================= LOG SERVER HTML =================

LOG_SERVER_HTML = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Logs ASCDROP - ASCITGROUP</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter', monospace;
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%);
            color:#22c55e;
            margin:0;
            padding:40px 30px;
            min-height:100vh;
        }
        .header {
            display:flex;
            align-items:center;
            gap:20px;
            margin-bottom:30px;
        }
        .logo {
            width:100px;
            height:auto;
        }
        h1 {
            color:#fff;
            font-weight:700;
            font-size:28px;
        }
        .subtitle {
            color:#9ca3af;
            font-size:14px;
            margin-bottom:25px;
        }
        .controls {
            margin-bottom:30px;
        }
        button {
            padding:10px 20px;
            margin:0 10px 10px 0;
            border:none;
            border-radius:10px;
            cursor:pointer;
            font-weight:600;
            font-size:14px;
            transition:all 0.2s;
        }
        .btn-download {
            background:linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color:#eff6ff;
        }
        .btn-clear {
            background:linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color:#fef2f2;
        }
        button:hover {
            transform:translateY(-1px);
            box-shadow:0 10px 25px rgba(0,0,0,0.4);
        }
        pre {
            background:rgba(17,24,39,0.95);
            backdrop-filter:blur(20px);
            padding:30px;
            border-radius:16px;
            overflow:auto;
            max-height:70vh;
            font-size:13px;
            line-height:1.5;
            border:1px solid rgba(34,197,94,0.3);
            white-space:pre-wrap;
            word-break:break-all;
        }
        .footer {
            text-align:center;
            margin-top:40px;
            padding-top:30px;
            border-top:1px solid rgba(59,130,246,0.3);
            font-size:12px;
            color:#6b7280;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/logo.png" alt="ASCITGROUP" class="logo">
        <div>
            <h1>ASCDROP - Audit Logs</h1>
            <div class="subtitle">Sistema de auditoría administrativa</div>
        </div>
    </div>

    <div class="controls">
        <form method="GET" action="/download_logs" style="display:inline;">
            <button class="btn-download">📥 Descargar Logs</button>
        </form>
        <form method="POST" action="/clear_logs" style="display:inline;">
            <button class="btn-clear">🗑️ Limpiar Logs</button>
        </form>
    </div>

    <pre>{{ logs }}</pre>

    <div class="footer">
        <strong>ASCITGROUP</strong><br>
        Protegiendo su infraestructura IT<br>
        <small>Creado por Marcos Hernández | <a href="https://www.linkedin.com/in/marcosh1488/" target="_blank" style="color:#60a5fa;">LinkedIn</a></small>
    </div>
</body>
</html>
"""

# ================= LOG SYSTEM =================

def rotate_logs():
    if os.path.exists(LOG_FILE):
        size_mb = os.path.getsize(LOG_FILE) / (1024 * 1024)
        if size_mb >= MAX_LOG_SIZE_MB:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.rename(LOG_FILE, f"activity_{timestamp}.log")

def log_event(action, filename="N/A"):
    rotate_logs()

    user = session.get("user", "unknown")
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    method = request.method
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = (
        f"{timestamp} | USER:{user} | IP:{ip} | "
        f"METHOD:{method} | ACTION:{action} | FILE:{filename} | "
        f"AGENT:{user_agent}\\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

# ================= AUTH =================

def auth_required():
    if "user" not in session:
        return False
    return True

# ================= LOGIN =================

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in USERS and USERS[u] == p:
            session["user"] = u
            log_event("LOGIN_SUCCESS")
            return redirect("/")
        else:
            log_event("LOGIN_FAILED")
    return LOGIN_HTML

@app.route("/logout")
def logout():
    log_event("LOGOUT")
    session.clear()
    return redirect("/login")

# ================= PANEL =================

@app.route("/")
def panel():
    if not auth_required():
        return redirect("/login")

    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(PANEL_HTML, files=files)

# ================= STATIC FILES (LOGO) =================

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# ================= SUBIDA =================

@app.route("/upload", methods=["POST"])
def upload():
    if not auth_required():
        return redirect("/login")

    for file in request.files.getlist("files"):
        if file.filename:
            name = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, name)
            file.save(path)
            log_event("UPLOAD", name)

    return redirect("/")

@app.route("/upload_folder", methods=["POST"])
def upload_folder():
    if not auth_required():
        return redirect("/login")

    files = request.files.getlist("folder")
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for file in files:
            safe_name = secure_filename(file.filename)
            zf.writestr(safe_name, file.read())

    name = "folder_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".zip"
    path = os.path.join(UPLOAD_FOLDER, name)

    with open(path, "wb") as f:
        f.write(zip_buffer.getvalue())

    log_event("UPLOAD_FOLDER", name)
    return redirect("/")

# ================= DESCARGA =================

@app.route("/download/<filename>")
def download(filename):
    if not auth_required():
        return redirect("/login")

    safe_name = secure_filename(filename)
    path = os.path.join(UPLOAD_FOLDER, safe_name)

    if not os.path.exists(path):
        log_event("DOWNLOAD_FAILED", safe_name)
        abort(404)

    log_event("DOWNLOAD", safe_name)
    return send_from_directory(UPLOAD_FOLDER, safe_name, as_attachment=True)

# ================= ELIMINAR =================

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    if not auth_required():
        return redirect("/login")

    safe_name = secure_filename(filename)
    path = os.path.join(UPLOAD_FOLDER, safe_name)

    if os.path.exists(path):
        os.remove(path)
        log_event("DELETE", safe_name)

    return redirect("/")

# ================= LOG SERVER =================

@app.route("/logserver")
def view_logs():
    if not auth_required() or session.get("user") != "Administrador":
        abort(403)

    if not os.path.exists(LOG_FILE):
        logs = "No hay registros aún."
    else:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.read().replace("<", "&lt;").replace(">", "&gt;")

    return render_template_string(LOG_SERVER_HTML, logs=logs)

@app.route("/download_logs")
def download_logs():
    if not auth_required() or session.get("user") != "Administrador":
        abort(403)

    if not os.path.exists(LOG_FILE):
        abort(404)

    return send_file(LOG_FILE, as_attachment=True)

@app.route("/clear_logs", methods=["POST"])
def clear_logs():
    if not auth_required() or session.get("user") != "Administrador":
        abort(403)

    open(LOG_FILE, "w").close()
    log_event("LOGS_CLEARED")
    return redirect("/logserver")

# ================= MAIN =================

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
