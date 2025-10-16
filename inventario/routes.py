
# routes.py — Módulo de rutas para manejar el inventario


from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db # 🔹 Importamos la función que maneja la base de datos

inventario_bp = Blueprint('inventario', __name__)


@inventario_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
            (nombre, precio, cantidad)
        )
        db.commit()
        db.close()

        return redirect(url_for('inventario.lista_productos'))

    return render_template('inventario/agregar_producto.html')


@inventario_bp.route('/lista')
def lista_productos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre, precio, cantidad FROM productos")
    productos = cursor.fetchall()
    db.close()
    return render_template('inventario/lista.html', productos=productos)


@inventario_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect(url_for('inventario.lista_productos'))



@inventario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    db= get_db()
    cursor= db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM productos WHERE id=?",(id,))
        producto= cursor.fetchone()
        db.close()
        return render_template('inventario/editar.html', producto=producto)
    elif request.method == 'POST':
        nombre = request.form['nombre']
        precio= request.form['precio']
        cantidad= request.form['cantidad']
        cursor.execute(
            "UPDATE productos SET nombre =?,precio=?,cantidad=? WHERE id=?",(nombre,precio,cantidad,id)
        )
        db.commit()
        db.close()
        return redirect(url_for('inventario.lista_productos'))

