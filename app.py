from flask import Flask,render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para mensajes flash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'tienda.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Producto(db.Model):
    __tablename__ = 'producto'
    id_prod = db.Column(db.Integer, primary_key=True)
    nom_prod = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id_prod': self.id_prod,
            'nom_prod': self.nom_prod,
            'estado': self.estado,
            'categoria': self.categoria,
            'precio': self.precio
        }

with app.app_context():
    db.create_all()
    if Producto.query.first() is None:
        producto1 = Producto(nom_prod='Laptop', estado='Nuevo', categoria='Electrónica', precio=1200.50)
        producto2 = Producto(nom_prod='Mesa', estado='Usado', categoria='Muebles', precio=200.00)
        db.session.add_all([producto1, producto2])
        db.session.commit()

# Mostrar todos los productos
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

# Formulario para agregar producto
@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nom_prod = request.form['nom_prod']
        estado = request.form['estado']
        categoria = request.form['categoria']
        try:
            precio = float(request.form['precio'])
        except ValueError:
            flash('Precio inválido', 'error')
            return redirect(url_for('nuevo_producto'))

        nuevo = Producto(nom_prod=nom_prod, estado=estado, categoria=categoria, precio=precio)
        db.session.add(nuevo)
        db.session.commit()
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('nuevo_producto.html')

# Formulario para editar producto
@app.route('/producto/editar/<int:id_prod>', methods=['GET', 'POST'])
def editar_producto(id_prod):
    producto = Producto.query.get_or_404(id_prod)
    if request.method == 'POST':
        producto.nom_prod = request.form['nom_prod']
        producto.estado = request.form['estado']
        producto.categoria = request.form['categoria']
        try:
            producto.precio = float(request.form['precio'])
        except ValueError:
            flash('Precio inválido', 'error')
            return redirect(url_for('editar_producto', id_prod=id_prod))
        db.session.commit()
        flash('Producto actualizado', 'success')
        return redirect(url_for('index'))
    return render_template('editar_producto.html', producto=producto)

# Eliminar producto
@app.route('/producto/eliminar/<int:id_prod>', methods=['POST'])
def eliminar_producto(id_prod):
    producto = Producto.query.get_or_404(id_prod)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
