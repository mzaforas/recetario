from flask import Flask, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


# Model
class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    elaboracion = db.Column(db.Text)
    tiempo_elaboracion = db.Column(db.Integer)
    numero_comensales = db.Column(db.Integer)
    origen = db.Column(db.String(45))
    coste = db.Column(db.Float)
    dificultad = db.Column(db.Integer)
    valoracion = db.Column(db.Integer)

    def __repr__(self):
        return '%s' % self.nombre


class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    unidad = db.Column(db.String(45))

    def __repr__(self):
        return '%s' % self.nombre


class IngredienteReceta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    cantidad = db.Column(db.Float)

    receta = db.relationship(Receta, backref="ingredientes")
    ingrediente = db.relationship(Ingrediente, backref="recetas")

admin = Admin(app)
admin.add_view(ModelView(Receta, db.session))
admin.add_view(ModelView(Ingrediente, db.session))

if __name__ == '__main__':
    app.run()