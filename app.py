"""Este es el desarrollo del Backend para la estructura de mitiendavirtual.com"""

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # ayuda a llevar de python a SQL

app = Flask(__name__)

#Configuración de base de datos 
#'postgresql://<usuario>:<contraseña>@<direccion de la db>:<puerto>/<nombre de la db>

#DB de ESTEBAN
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pololo@localhost:5432/tiendavirtualdb'

#DB HEROKU
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hpxwwhitjtynjd:fad084c3db4bf0573bdc0d5e20d54fe0709408c629e9e43fca9c4eeefe3bf859@ec2-54-174-172-218.compute-1.amazonaws.com:5432/dchtn7qs3oiffk'

#DB de LINA
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/tiendavirtualdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some-secret-key'

#Definimos la base de datos
db =  SQLAlchemy(app) 

#Importamos los modelos
from models import Shopowner, Product

#Creamos el esquema de la base de datos
db.create_all()
db.session.commit()

#Creamos las diferentes rutas

#Ruta para el home
@app.route('/')
def hello():
    return render_template("home.html")

#Ruta para el registro de usuario nuevo (tendero)
@app.route('/register')
def register():
    return render_template("signup.html")

#Registro de usuario en la base de datos
@app.route('/create_user', methods=['POST'])
def create_user():
    request_data = request.form
    name = request_data["Nombres"]
    last_name = request_data["Apellidos"]
    email = request_data["Email"]
    password = request_data["Contraseña"]
    store_type = request_data["Tipo de tienda"]
    
    shopowner = Shopowner(name, last_name, email, password, store_type)
    db.session.add(shopowner)
    db.session.commit()
    
    print("Nombre:" + name)
    print("Apellido:" + last_name)
    print("Email:" + email)
    print("Contraseña:" + password)
    print("Tipo de tienda:" + store_type)
    
    #id = shopowner.id

    return redirect(url_for('register_inventory'))


# REGISTRO DE INVENTARIO Y PRODUCTOS EN PROCESO DE ELABORACIÓN
#Ruta para registro de inventario
@app.route('/register_inventory/<user>') #revisar con Rubén <----------------------------
def register_inventory(user):
    return render_template("inventory.html", user=user)

#Registro de productos al inventario
@app.route('/product', methods=['POST'])
def product():
    request_data = request.form
    product = request_data['Producto']
    category = request_data['Categoría']
    unit = request_data['Unidad']
    unit_price = request_data['Precio unidad']
    shopowner_id=Shopowner.query.filter(Shopowner.id)

    
    entry = Product(product,category,unit,unit_price,shopowner_id)
    db.session.add(entry)
    db.session.commit()

    print("Producto:" + product)
    print("Categoría:" + category)
    print("Unidad de producto:" + unit)
    print("Precio unidad:" + unit_price)
    print("ID Tendero:" + shopowner_id)


    return 'Se registró el producto exitosamente'
    
#Ruta para ver el inventario
@app.route('/inventory')
def inventory():
    return "Esta es la página que muestra el inventario de la tienda"

# Ruta para ingresar el usuario
@app.route('/login')
def login():
    return render_template("login.html")

# Ruta de logueo de usuario
@app.route('/check_user', methods=['POST'])
def check_user():
    request_data = request.form
    email = request_data["Email"]
    password = request_data["Contraseña"]
    user=Shopowner.query.filter(Shopowner.password==password,Shopowner.email==email)

    try:
        if(user[0] is not None):
            return render_template("inventory.html")

    except:
        return render_template("login.html")


#PRUEBA PARA CSS
@app.route('/prueba')
def prueba():
    return render_template("pruebacss.html")


"""------------------------------------------------------------------ 
Las rutas definidas a continuación están previstas para desarrollo posterior

#Ruta para mostrar el perfil del nuevo usuario
@app.route('/profile/<users>')
def profile(users):
    return render_template("profile.html", users=users)
    
#Ruta para modificación de datos personales del usuario (por ahora está manual - falta desarrollo con HTML y POST)
@app.route('/update_shopowner')
def update_shopowner():
    old_name = "María"
    new_name = "José"
    old_song = Shopowner.query.filter_by(name=old_name).first()
    old_song.name = new_name
    db.session.commit()
    return "actualización exitosa"

#Ruta para login
@app.route('/login/<user>')
def login(user):
    return render_template("profile.html", user=user)

@app.route('/accounting_flow')
def utilities():
    return "Esta es la página que muestra el los movimientos"

@app.route('/alerts')
def alerts():
    return "Esta es la página que permite configurar y ver las alertas de reposición y deudores"

@app.route('/invoices')
def orders():
    return "Esta es la página que permite registrar facturas y deudores"
--------------------------------------------------------------------------"""


if __name__ == "__main__":
    app.run()



