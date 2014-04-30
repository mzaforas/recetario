from flask import Flask, redirect, render_template, request, flash, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from wtforms import Form, BooleanField, TextField, PasswordField, validators, IntegerField, TextAreaField, FloatField

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)

### Models ###


class Receta(db.Model):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    elaboracion = Column(Text)
    ingredientes = Column(Text)
    tiempo_elaboracion = Column(Integer)
    numero_comensales = Column(Integer)
    origen = Column(String(45))
    coste = Column(Float)
    dificultad = Column(Integer)
    valoracion = Column(Integer)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '%s' % self.nombre


#class Ingrediente(db.Model):
#    __tablename__ = 'ingredientes'
#
#    id = Column(Integer, primary_key=True)
#    nombre = Column(String(45), nullable=False)
#    unidad = Column(String(45))
#
#    def __repr__(self):
#        return '%s' % self.nombre
#
#
#class IngredienteReceta(db.Model):
#    __tablename__ = 'ingredientesrecetas'
#
#    id = Column(Integer, primary_key=True)
#    receta_id = Column(Integer, ForeignKey('recetas.id'))
#    ingrediente_id = Column(Integer, ForeignKey('ingredientes.id'))
#    cantidad = Column(Float)
#
#    receta = relationship(Receta, backref="ingredientes")
#    ingrediente = relationship(Ingrediente, backref="recetas")


class Tag(db.Model):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)


Table('tagsrecetas', db.Model.metadata,
      Column('tag_id', Integer, ForeignKey('tags.id')),
      Column('receta_id', Integer, ForeignKey('recetas.id')))

### Forms ###


class RecetaForm(Form):
    nombre = TextField(validators=[validators.Length(max=80)])
    ingredientes = TextAreaField()
    elaboracion = TextAreaField()
    tiempo_elaboracion = IntegerField(validators=[validators.optional()])
    numero_comensales = IntegerField(validators=[validators.optional(), validators.NumberRange(min=1, max=20)])
    origen = TextField(validators=[validators.optional(), validators.Length(max=45)])
    coste = FloatField(validators=[validators.optional()])
    dificultad = IntegerField(validators=[validators.optional(), validators.NumberRange(min=1, max=10)])
    valoracion = IntegerField(validators=[validators.optional(), validators.NumberRange(min=1, max=10)])

### Controllers ###


@app.route('/')
def index():
    recetas = Receta.query.order_by(Receta.id).limit(10).all()
    return render_template('index.html', recetas=recetas)


@app.route('/insertar', methods=['GET', 'POST'])
def insertar():
    form = RecetaForm(request.form)
    if request.method == 'POST' and form.validate():
        receta = Receta(**{field.name: field.data for field in form})
        db.session.add(receta)
        db.session.commit()
        flash(u'Receta guardada')
        return redirect(url_for('index'))
    return render_template('formulario.html', form=form)


@app.route('/modificar/<id>', methods=['GET', 'POST'])
def modificar(id):
    receta = Receta.query.get(id)
    form = RecetaForm(request.form, receta)

    if request.method == 'POST' and form.validate():
        receta.update(**{field.name: field.data for field in form})
        db.session.add(receta)
        db.session.commit()
        flash(u'Receta guardada')
        return redirect(url_for('index'))
    return render_template('formulario.html', form=form, receta=receta)

if __name__ == '__main__':
    app.run()

