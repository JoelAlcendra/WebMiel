from flask import Flask, render_template
from flask_migrate import Migrate
from database import db
from models import Product, User, Order, OrderItem


app = Flask(__name__)

# CONFIGURACION/CONEXION A LA BASE DE DATOS
USER_DB = 'postgres'
USER_PASSWORD = '1234'
SERVER_DB = 'localhost'
NAME_DB = 'demo'


FULL_URL_DB = f'postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB

db.init_app(app)


# CONFIGURACION DE MIGRACIONES
migrate = Migrate()
migrate.init_app(app, db)


@app.route('/')
def inicio():
    products = Product.query.all()
    total_products = Product.query.count()
    return render_template('index.html', datos=products, total=total_products)





