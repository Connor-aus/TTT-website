from . import db

class Category(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'scroll1.jpg')
    products = db.relationship('Product', backref='Category', cascade="all, delete-orphan")

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}\n" 
        str =str.format( self.id, self.name,self.description,self.image)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('product_id',db.Integer,db.ForeignKey('products.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'product_id') )

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    subcat = db.Column(db.String(64), nullable=True)
    ac = db.Column(db.String(64), nullable=True)
    prereq = db.Column(db.String(64), nullable=True)
    stealth = db.Column(db.String(64), nullable=True)
    weight = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}, Price: {}, Category: {}, Sub-category: {}, Armour Class: {}, Prerequisite: {}, Stealth: {}, Weight: {}\n" 
        str =str.format( self.id, self.name, self.description, self.image, self.price, self.category_id, self.subcat, self.ac, self.prereq, self.stealth, self.weight, )
        return str

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    avatarname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    totalcost = db.Column(db.Float)
    products = db.relationship("Product", secondary=orderdetails, backref="orders")
    
    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Avater name: {}, Email: {}, Poducts: {}, Total Cost: {}\n" 
        str =str.format( self.id, self.status, self.firstname, self.surname, self.avatarname, self.email, self.products, self.totalcost)
        return str
