from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy # ayuda a llevar de python a SQL

app = Flask(__name__)

#configuración de base de datos 
#buena práctica es crear un archivo config.py con esta configuración, pero puede ir aquí también
#'postgresql://<usuario>:<contraseña>@<direccion de la db>:<puerto>/<nombre de la db>

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/tiendavirtualdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some-secret-key'

db =  SQLAlchemy(app) #definimos la base de datos

#Importar los modelos
from models import Shopowner, Product

#crear el esquema de la base de datos
db.create_all()
db.session.commit()

@app.route('/')
def hello():
    return render_template("index.html")

#por defecto, el método http que python interpreta, es GET
#por eso es que en el terminal sale el verbo GET al momento de iniciar flask y hacer el request


#rutas de páginas

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/profile')
def profile():
    
    return "Esta es el página para el perfil con los datos del tendero y la tienda"

@app.route('/inventory')
def inventory():
    return "Esta es la página que muestra el inventario de la tienda"

@app.route('/accounting_flow')
def utilities():
    return "Esta es la página que muestra el los movimientos"

@app.route('/alerts')
def alerts():
    return "Esta es la página que permite configurar y ver las alertas de reposición y deudores"

@app.route('/invoices')
def orders():
    return "Esta es la página que permite registrar facturas y deudores"



#rutas de otras acciones
# decorador "@" - agregar funcionalidad extra a un métodoo o función


#INFORMACIÓN DE REGISTRO DEL TENDERO

@app.route('/shop_owner', methods=['GET','POST'])
def crud_shopowner():
    if request.method == 'GET':
        # Hago algo
        print("Llegó un GET")

        # Inserción de prueba en la DB
        name = "Pepito"
        last_name = "Ramírez"
        email = "pepito.perez@gmail.com"
        password= "12345"
        store_type = "Víveres"

        entry = Shopowner(name,last_name,email,password,store_type)
        db.session.add(entry)
        db.session.commit()
        return 'Esto fue un GET'

    elif request.method == 'POST':
        # Registrar una cancion
        request_data = request.form
        name = request_data['name']
        last_name = request_data['last name']
        store_type = request_data['store type']

        print("Nombre:" + name)
        print("Apellido:" + last_name)
        print("Tipo de Tienda:" + store_type)

        # Insertar en la base de datos la canción
        return 'Se registro el tendero exitosamente'

@app.route('/update_shopowner')
def update_shopowner():
    old_name = "María"
    new_name = "José"
    old_song = Shopowner.query.filter_by(name=old_name).first()
    old_song.name = new_name
    db.session.commit()
    return "actualización exitosa"


# INFORMACIÓN DE REGISTRO DE PRODUCTO PRODUCTO

@app.route('/product', methods=['GET','POST'])
def crud_product():
    if request.method == 'GET':
        # Hago algo
        print("Llegó un GET")

        # Inserción de prueba en la DB
        product = "Chocorramo"
        category = "Pastelería"
        unit = "Unidad"
        unit_price = 1000

        entry = Product(product,category,unit,unit_price)
        db.session.add(entry)
        db.session.commit()
        return 'Esto fue un GET'

    elif request.method == 'POST':
        # Registrar una cancion
        request_data = request.form
        id = request_data['id de producto']
        product = request_data['producto']

        print("Producto:" + product)
        print("Precio total:" + total_price)

        # Insertar en la base de datos la canción
        return 'Se registro el producto exitosamente'




