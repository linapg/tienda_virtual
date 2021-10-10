"""Este es el desarrollo del Backend para la estructura de mitiendavirtual.com"""

from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#----------------< Configuración de base de datos >------------------

#'postgresql://<usuario>:<contraseña>@<direccion de la db>:<puerto>/<nombre de la db>

#DB de ESTEBAN
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pololo@localhost:5432/tiendavirtualdb'

#DB HEROKU
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hpxwwhitjtynjd:fad084c3db4bf0573bdc0d5e20d54fe0709408c629e9e43fca9c4eeefe3bf859@ec2-54-174-172-218.compute-1.amazonaws.com:5432/dchtn7qs3oiffk'

#DB de LINA
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/mitienda_virtualdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some-secret-key'

#Definimos la base de datos
db =  SQLAlchemy(app) 

#Importamos los modelos
from models import Shopowner, Product, Inventory

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
    return render_template("register.html")

#Registro de usuario en la base de datos - CRUD
@app.route('/create_user', methods=['POST'])
def create_user():
    request_data = request.form
    name = request_data["Nombres"]
    last_name = request_data["Apellidos"]
    email = request_data["Email"]
    password = request_data["Contraseña"]
    store_type = request_data["Tipo de tienda"]
    
    email_list = list(email)
    
    if name is None:
        print("name is empty")
        return render_template("error_in_register.html")
    elif last_name is None:
        print("last name is empty")
        return render_template("error_in_register.html")
    elif "@" and "." not in email_list:
        print("email error")
        return render_template("error_in_register.html")
    elif email is None:
        print("email empty")
        return render_template("error_in_register.html")
    elif password is None:
        print("password empty")
        return render_template("error_in_register.html")
    elif store_type is None:
        print("store_type empty")
        return render_template("error_in_register.html")
        
    else:
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
        
        return redirect(url_for('control_center'))
    
#Ruta para el login 
@app.route('/login')
def login():
    return render_template("login.html")

#Ruta para el centro de control
@app.route('/control_center')
def control_center():
    user=Shopowner.query.get(session['user_id'])
    return render_template("control_center.html", user=user)

#Ruta para mostrar el profile
@app.route('/profile')
def profile():
    user=Shopowner.query.get(session['user_id'])
    return render_template("profile.html", user=user)

# Ruta de logueo de usuario
@app.route('/check_user', methods=['POST'])
def check_user():
    request_data = request.form
    email = request_data["Email"]
    password = request_data["Contraseña"]
    user=Shopowner.query.filter(Shopowner.password==password,Shopowner.email==email)

    print(user)

    if (len(list(user)) == 1):
        session['user_id'] =user[0].id
        print("should send to profile")
        return render_template("control_center.html", user=user[0])

    else:
        return render_template("userdata_notfound.html")
        
    
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
    #shopowner_id=Shopowner.query.filter(Shopowner.id)
    #print(shopowner_id)
    shopowner_id = session['user_id']
    
    entry = Product(product,category,unit,shopowner_id)
    db.session.add(entry)
    db.session.commit()
    
    print("id usuario: " + str(session['user_id']))
    print("Producto: " + product)
    print("Categoría: " + category)
    print("Unidad de producto: " + unit)
    print("ID Tendero: " + str(shopowner_id))

    return render_template("register_inventory.html")
    
#Ruta para formulario de registro en el inventario
@app.route("/register_inventory")
def register_inventory():
    return render_template("iregister_inventory.html")

#Ruta para añadir información de producto al inventario
@app.route("/feed_inventory")
def feed_inventory():
    request_data = request.form
    date = request_data['Fecha']
    entry = request_data['Cantidad de entrada de producto']
    unit_cost = request_data['Costo unidad']
    selling_price = request_data['Precio de venta']
    supplier = request_data['Proveedor']

    #shopowner_id=Shopowner.query.filter(Shopowner.id)
    #print(shopowner_id)
    shopowner_id = session['user_id']
    
    total_quantity = 0
    total_inventory_cost = entry * unit_cost
    profit_per_unit = selling_price - unit_cost
    total_profit = profit_per_unit * total_quantity
    
    entry_inventory = Inventory(date,entry,unit_cost,total_quantity,total_inventory_cost,selling_price,profit_per_unit,total_profit,supplier)
    db.session.add(entry_inventory)
    db.session.commit()
    
    print("id usuario: " + str(session['user_id']))
    print("Cantidad de entrada " + str(entry))
    print("Costo unidad: " + str(unit_cost))
    print("Precio de venta:" + str(selling_price))
    print("Precio unidad:" + str(unit_cost))
    print("Proveedor: " + supplier)
    print("Cantidad total:" + str(total_quantity))
    print("Costo total inventario:" + str(total_inventory_cost))
    print("Ganancia por unidad:" + str(profit_per_unit))
    print("Ganancia total:" + str(total_profit))

    return render_template("inventory.html")

#Ruta para ver el inventario
@app.route('/inventory')
def inventory():
    inventory_data = db.session.query(Product).all()
    print(inventory_data)
    return render_template("inventory.html", inventory_data=inventory_data)


# ---< Otras rutas a desarrollar si hay tiempo >--

@app.route('/accounting_flow')
def accounting_flow():
    return render_template("accounting_flow.html")

@app.route('/debtors')
def debtors():
    return render_template("debtors.html")

@app.route('/invoices')
def invoices():
    return render_template("invoices.html")


# ---< Rutas para prueba de CSS >--

@app.route('/prueba')
def prueba():
    return render_template("pruebacss.html")

if __name__ == "__main__":
    app.run()



