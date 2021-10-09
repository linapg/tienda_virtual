from app import db

class Shopowner(db.Model):
    __tablename__ = 'Shopowner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50), nullable=True) # <-- Revisar si al cambiar aquí, hay que cambiar en Postgres también?
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
    product = db.Column(db.String, unique=False)
    category = db.Column(db.String)
    unit = db.Column(db.String)
    unit_price= db.Column(db.Integer)
    shopowner_id = db.Column(db.ForeignKey("Shopowner.id")) # <-- Añadido 04.10

    def __init__(self,product,category,unit,unit_price,shopowner_id):
        self.product = product
        self.category = category
        self.unit = unit
        self.unit_price = unit_price
        self.shopowner_id = shopowner_id 

class Inventory(db.Model):
    __tablename__ = 'Inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    product_id = db.Column(db.ForeignKey("Product.id"))
    initial_inventory = db.Column(db.Integer)
    shelves_quantity = db.Column(db.Integer, nullable=True) #no los usaremos ahora
    shelves_minimun = db.Column(db.Integer, nullable=True) #no los usaremos ahora
    entries = db.Column(db.Integer)
    consumption = db.Column(db.Integer)
    final_inventory = db.Column(db.Integer, nullable=True) #no los usaremos ahora
    bare_minimum = db.Column(db.Integer, nullable=True) #no los usaremos ahora
    unit_cost = db.Column(db.Integer)
    total_inventory_cost = db.Column(db.Integer)
    
    def __init__(self,date,product_id,initial_inventory,shelves_quantity,shelves_minimun,entries,consumption,final_inventory,bare_minimum,unit_cost,total_inventory_cost):
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
        

class AccountingFlow(db.Model):
    __tablename__ = 'AccountingFlow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    total_sales = db.Column(db.Integer)
    cost_of_sale = db.Column(db.Integer)
    expenses = db.Column(db.Integer)
    taxes = db.Column(db.Integer)
    profits = db.Column(db.Integer)

    def __init__(self, date, total_sales, cost_of_sale, expenses, taxes, profits):
        self.date = date
        self.total_sales = total_sales
        self.cost_of_sale = cost_of_sale
        self.expenses = expenses
        self.taxes = taxes
        self.profits = profits

class Invoice(db.Model):
    __tablename__ = 'Invoice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    product_id = db.Column(db.ForeignKey("Product.id"))
    q_sold = db.Column(db.Integer)
    payment_meth = db.Column(db.String)
    tot_sales = db.Column(db.Integer)
    def __init__(self, date, product_id, q_sold, payment_meth, tot_sales):
        self.date = date
        self.product_id = product_id
        self.q_sold = q_sold
        self.payment_meth = payment_meth
        self.tot_sales = tot_sales

class ProductInvoice(db.Model):
    __tablename__ = 'ProductInvoice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.ForeignKey("Product.id"))
    invoice_id = db.Column(db.ForeignKey("Invoice.id"))
    def __init__(self, product_id, invoice_id):
        self.product_id = product_id
        self.invoice_id = invoice_id

class Receivables(db.Model):
    __tablename__ = 'Receivables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.Integer)
    email = db.Column(db.Integer, unique=True)
    invoice_id = db.Column(db.ForeignKey("Invoice.id"))
    deadline = db.Column(db.DateTime)
    def __init__(self, name, address, phone, email, invoice_id, deadline):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.invoice_id = invoice_id
        self.deadline = deadline



