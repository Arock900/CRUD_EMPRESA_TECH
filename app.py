from flask import Flask, render_template
from inventario import inventario_bp  # Importamos el Blueprint
from usuarios import usuarios_bp


app = Flask(__name__)

app.secret_key="clave_super_secreta_1234"


# Registramos el Blueprint de inventario
app.register_blueprint(inventario_bp, url_prefix="/inventario")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

