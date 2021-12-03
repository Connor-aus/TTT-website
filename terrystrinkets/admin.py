'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

In the terminal navigate to the project folder just above the miltontours package
Type 'python' to enter the python interpreter. You should see '>>>'
In python interpreter type the following (hitting enter after each line):
    from miltontours import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------

# Option 1: Use DB Browser for SQLite
You can enter data directly into the cities or tours table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2020-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from . import db
from .models import Category, Product, Order


bp = Blueprint('admin', __name__, url_prefix='/admin/')

# function to put some seed data in the database
@bp.route('/dbseed/')
def dbseed():
    category1 = Category(name='Armour', image='armours1.png', \
        description='''Browse the finest selection of armours here. Whether you're on the front line fighting for your life, or at the back hiding behind your friends, you can never have too much protection!''')
    category2 = Category(name='Weapons', image='weaponcat1.jpg', \
        description='''Looking to cleave your foes in twain? Maybe squash them with a greathammer? Either way, offense is the best defense, and we have all of your offensive needs right here!''')
    category3 = Category(name='Magic Items', image='wandcat1.jpg', \
        description='''Here is where you will find our wide selection of magical paraphernalia. From casting spells to shielding from them, you can scratch all of your magical itches right here!''')
    category4 = Category(name='Tools', image='tools1.png', \
        description='''Ever wondered how thiefs go about picking locks, or how blacksmiths mend your armour? If you're the entrepreneurial type looking to rustle up your own little venture, then we've got you sorted!''')
      
    try:
        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.add(category4)
        db.session.commit()
    except:
        return 'There was an issue adding the categories in dbseed function'

    armourl1 = Product(category_id=category1.id, image='armorpadded.png', price=5,\
        subcat='Light Armour',\
        name='Padded Armour',\
        ac='11 + Dex modifier',\
        prereq='-',\
        stealth='Disadvantage',\
        weight='8 lb.',\
        description='Padded armour consists of quilted layers of cloth and batting.') 
    armourl2 = Product(category_id=category1.id, image='armorleather.png', price=10,\
        subcat='Light Armour',\
        name='Leather Armour',\
        ac='11 + Dex modifier',\
        prereq='-',\
        stealth='-',\
        weight='10 lb.',\
        description='Some of this armour is made of leather that has been stiffened by being boiled in oil. The rest is made of softer and more flexible materials.')
    armourl3 = Product(category_id=category1.id, image='armorstudded.png', price=45,\
        subcat='Light Armour',\
        name='Studded Leather Armour',\
        ac='12 + Dex modifier',\
        prereq='-',\
        stealth='-',\
        weight='13 lb.',\
        description='Made from tough but flexible leather, studded leather is reinforced with close-set rivets or spikes.')
    armourm1 = Product(category_id=category1.id, image='armorhide.png', price=10,\
        subcat='Medium Armour',\
        name='Hide Armour',\
        ac='12 + Dex modifier',\
        prereq='-',\
        stealth='-',\
        weight='12 lb.',\
        description='This crude armour consists of thick furs and pelts.')
    armourm2 = Product(category_id=category1.id, image='armorchainshirt.png', price=50,\
        subcat='Medium Armour',\
        name='Chain Shirt',\
        ac='13 + Dex modifier',\
        prereq='-',\
        stealth='-',\
        weight='20 lb.',\
        description='Made of interlocking metal rings, a chain shirt is worn between layers of clothing or leather. This armour offers modest protection to the wearer’s upper body.')
    armourm3 = Product(category_id=category1.id, image='armorscale.png', price=50,\
        subcat='Medium Armour',\
        name='Scale Armour',\
        ac='14 + Dex modifier',\
        prereq='-',\
        stealth='Disadvantage',\
        weight='45 lb.',\
        description='This armour consists of a coat and leggings (and perhaps a separate skirt) of leather covered with overlapping pieces of metal, much like the scales of a fish.')
    armourm4 = Product(category_id=category1.id, image='armorbreastplate.png', price=400,\
        subcat='Medium Armour',\
        name='Breastplate Armour',\
        ac='14 + Dex modifier',\
        prereq='-',\
        stealth='-',\
        weight='20 lb.',\
        description='This armour consists of a fitted metal chest piece worn with supple leather. Although it leaves the legs and arms relatively unprotected, this armour provides good protection for the wearer’s vital organs.')
    armourm5 = Product(category_id=category1.id, image='armorhalfplate.png', price=750,\
        subcat='Medium Armour',\
        name='Half Plate Armour',\
        ac='15 + Dex modifier',\
        prereq='13 Str',\
        stealth='Disadvantage',\
        weight='40 lb.',\
        description='Half plate consists of shaped metal plates that cover most of the wearer’s body. It does not include leg protection beyond simple greaves that are attached with leather straps.')

    try:
        db.session.add(armourl1)
        db.session.add(armourl2)
        db.session.add(armourl3)
        db.session.add(armourm1)
        db.session.add(armourm2)
        db.session.add(armourm3)
        db.session.add(armourm4)
        db.session.add(armourm5)
        db.session.commit()
    except:
        return 'There was an issue adding a product in dbseed function'

    return 'DATA LOADED'


