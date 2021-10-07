"""Este es el desarrollo del Backend para la estructura de mitiendavirtual.com"""

from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy # ayuda a llevar de python a SQL

app = Flask(__name__)

#----------------< Configuración de base de datos >------------------

#'postgresql://<usuario>:<contraseña>@<direccion de la db>:<puerto>/<nombre de la db>

#DB de ESTEBAN
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pololo@localhost:5432/tiendavirtualdb'

#DB HEROKU
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hpxwwhitjtynjd:fad084c3db4bf0573bdc0d5e20d54fe0709408c629e9e43fca9c4eeefe3bf859@ec2-54-174-172-218.compute-1.amazonaws.com:5432/dchtn7qs3oiffk'

#DB de LINA
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/tiendavirtualdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some-secret-key'

#Definimos la base de datos
db =  SQLAlchemy(app) 

#Importamos los modelos
from models import Shopowner, Product

#Creamos el esquema de la base de datos
db.create_all()
db.session.commit()


#-------------< Rutas >------------------------

# ---< Rutas para el usuario >---


#Ruta para el home
@app.route('/')
def hello():
    return render_template("home.html")

#Ruta para el formulario de registro de usuario nuevo
@app.route('/register')
def register():
    return render_template("signup.html")

#Registro de usuario en la base de datos - CRUD
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
    
    #diccionario volatil del servidor - sirve para uso de info en varios endpoints
    session['user_id'] =shopowner.id
    
    print("Nombre:" + name)
    print("Apellido:" + last_name)
    print("Email:" + email)
    print("Contraseña:" + password)
    print("Tipo de tienda:" + store_type)
    print(session['user_id'])

    return redirect(url_for('profile'))

#Ruta para login
@app.route('/perfil')
def perfil():
    user=Shopowner.query.get(session['user_id'])

    return render_template("profile.html", data_user=user)

# Ruta de logueo de usuario
@app.route('/check_user', methods=['POST'])
def check_user():
    request_data = request.form
    email = request_data["Email"]
    password = request_data["Contraseña"]
    user=Shopowner.query.filter(Shopowner.password==password,Shopowner.email==email)

    try:
        if(user[0] is not None):
            session['user_id'] =user[0].id
            return render_template("profile.html")

    except:
        return render_template("login.html")
    

#Ruta para mostrar el perfil del usuario
@app.route('/perfilhtml')
def perfilhtml():
    return render_template("profile.html")

#Ruta para modificación de datos personales del usuario (por ahora está manual - falta desarrollo con HTML y POST)
@app.route('/update_shopowner')
def update_shopowner():
    old_name = "María"
    new_name = "José"
    old_song = Shopowner.query.filter_by(name=old_name).first()
    old_song.name = new_name
    db.session.commit()
    return "actualización exitosa"

#RUTA CERRAR SESIÓN
#session.pop('user_id', None)

# ---< Rutas para productos e inventario >--


#Ruta para registro de productos
@app.route('/register_product') 
def register_product():
    return render_template("register_product.html")

#Registro de productos en el inventario - CRUD
@app.route('/product', methods=['POST'])
def product():
    request_data = request.form
    product = request_data['Producto']
    category = request_data['Categoría']
    unit = request_data['Unidad']
    unit_price = request_data['Precio unidad']
    #shopowner_id=Shopowner.query.filter(Shopowner.id)
    #print(shopowner_id)
    shopowner_id = session['user_id']
    
    entry = Product(product,category,unit,unit_price,shopowner_id)
    db.session.add(entry)
    db.session.commit()
    
    print("id usuario" + str(session['user_id']))
    print("Producto:" + product)
    print("Categoría:" + category)
    print("Unidad de producto:" + unit)
    print("Precio unidad:" + unit_price)
    print("ID Tendero:" + str(shopowner_id))


    return render_template("inventory.html")
    
#Ruta para ver el inventario
@app.route('/inventory')
def inventory():
    return render_template("inventory.html")


# ---< Otras rutas a desarrollar si hay tiempo >--


@app.route('/accounting_flow')
def utilities():
    return "Esta es la página que muestra el los movimientos"

@app.route('/alerts')
def alerts():
    return "Esta es la página que permite configurar y ver las alertas de reposición y deudores"

@app.route('/invoices')
def orders():
    return "Esta es la página que permite registrar facturas y deudores"



# ---< Rutas para prueba de CSS >--

@app.route('/prueba')
def prueba():
    return render_template("pruebacss.html")

if __name__ == "__main__":
    app.run()



