from flask import Blueprint

usuarios_bp = Blueprint(
    "usuarios",
    __name__,
    template_folder="../templates/usuarios"  # 👈 clave: subcarpeta correcta
)

from . import routes
