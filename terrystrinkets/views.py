from itertools import product
from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Category, Product, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', categories = categories)

@bp.route('/armour/')
def armour():
    products = Product.query.filter(Product.category_id).all()
    return render_template('armour.html', products = products)

@bp.route('/products/')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    products = Product.query.filter(Product.name.like(search)).all()
    products = Product.query.filter(Product.subcat.like(search)).all()
    products = Product.query.filter(Product.description.like(search)).all()
    products = Product.query.filter(Product.price.like(search)).all()
    return render_template('armour.html', products = products)

# Referred to as "cart" to the user
@bp.route('/order', methods=['POST','GET'])
def order():
    product_id = request.values.get('product_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', avatarname='', email='', totalcost=0 )
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for product in order.products:
            totalprice = totalprice + product.price
    
    # are we adding an item?
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
            except:
                return 'My apologies, I am afraid there was an issue adding the item to your cart.'
            return redirect(url_for('main.order'))
        else:
            flash('My noble adventurer, that item is already in your cart.')
            return redirect(url_for('main.order'))
    
    return render_template('order.html', order = order, totalprice = totalprice)


# Delete specific cart items
@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        product_to_delete = Product.query.get(id)
        try:
            order.products.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'It seems there was a problem removing the item from your order.'
    return redirect(url_for('main.order'))


# Scrap cart
@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('Very well. Jarvis will see that your items are returned to their correct position.')
    return redirect(url_for('main.index'))


@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.avatarname = form.avatarname.data
            order.email = form.email.data
            totalcost = 0
            for product in order.products:
                totalcost = totalcost + product.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('We greatly appreciate your patronage. Jarvis will deliver the items and the invoice to your address post haste...')
                return redirect(url_for('main.index'))
            except:
                return 'It seems there was an issue completing your order. Guards!!!'
    return render_template('checkout.html', form = form)