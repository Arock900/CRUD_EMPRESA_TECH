from flask import render_template, request, redirect, url_for, session, flash
from . import usuarios_bp

# --- LOGIN ---
@usuarios_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("email")
        contrasena = request.form.get("password")

        print(f"📩 Datos recibidos -> usuario: {usuario}, contraseña: {contrasena}")

        if usuario == "andresrojas900@gmail.com" and contrasena == "1234":
            print("✅ Credenciales correctas, debería redirigir al dashboard")
            session["usuario"] = usuario
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("usuarios.dashboard"))
        else:
            print("❌ Credenciales incorrectas, redirigiendo al login")
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for("usuarios.login"))

    return render_template("usuarios/login.html")

# --- DASHBOARD ---
@usuarios_bp.route("/dashboard")
def dashboard():
    if "usuario" in session:
        usuario = session["usuario"]
        # ✅ igual, indicando la subcarpeta
        return render_template("usuarios/dashboard.html", usuario=usuario)
    else:
        flash("Debes iniciar sesión para acceder al dashboard", "warning")
        return redirect(url_for("usuarios.login"))

# --- LOGOUT ---
@usuarios_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("usuarios.login"))

# --- REGISTRO ---
@usuarios_bp.route("/registro")
def registro():
    return render_template("usuarios/registro.html")
