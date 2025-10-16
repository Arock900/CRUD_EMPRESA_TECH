from flask import Blueprint

# Definimos el Blueprint
inventario_bp = Blueprint(
    "inventario",
    __name__,
    template_folder="templates"
)

# Importamos las rutas
from .routes import *
__all__=["inventario_bp"]

