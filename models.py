from app import db

# Tabla Tendero
class Shopowner(db.Model):
    __tablename__ = 'Shop Owner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50), nullable=True)
    store_type = db.Column(db.String, nullable=True)

    def __init__(self,name,last_name,email,password,store_type):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.store_type = store_type

class Product(db.Model):
    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.Column(db.String, unique=True)
    category = db.Column(db.String)
    unit = db.Column(db.String)
    unit_price= db.Column(db.Integer)
    
    def __init__(self,id,product,category,unit,unit_price):
        self.id = id
        self.product = product
        self.category = category
        self.unit = unit
        self.unit_price = unit_price

class Inventory(db.Model):
    __tablename__ = 'Inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    product_id = db.Column(db.ForeignKey("Product.id"))
    initial_inventory = db.Column(db.Integer)
    shelves_quantity = db.Column(db.Integer)
    shelves_minimun = db.Column(db.Integer)
    entries = db.Column(db.Integer)
    consumption = db.Column(db.Integer)
    final_inventory = db.Column(db.Integer)
    bare_minimum = db.Column(db.Integer)
    unit_cost = db.Column(db.Integer)
    total_inventory_cost = db.Column(db.Integer)
    
    def __init__(self,id,date,product_id,initial_inventory,shelves_quantity,shelves_minimun,entries,consumption,final_inventory,bare_minimum,unit_cost,total_inventory_cost):
        self.id = id
        self.date = date
        self.product_id = product_id
        self.initial_inventory = initial_inventory
        self.shelves_quantity = shelves_quantity
        self.shelves_minimun = shelves_minimun
        self.entries = entries
        self.consumption = consumption
        self.final_inventory = final_inventory
        self.bare_minimum = bare_minimum
        self.unit_cost = unit_cost
        self.total_inventory_cost = total_inventory_cost
        
        
