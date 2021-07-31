from flask import Flask
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(128))

    def __repr__(self):
        return f'{self.name} - {self.description}'

@app.route('/')
def index():
    return "hello"

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {'name': drink.name,'description': drink.description}
        output.append(drink_data)

    return {'dinks':output}

@app.route('/drinks/<id>')
def get_drink(id):
     drink = Drink.query.get_or_404(id)
     return {"name":drink.name, "description": drink.description}

@app.route('/drinks', methods=['POTST'])
def  add_drink():
    drink = Drink(name=Request.json['name']), description=Request.json['description')]
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route(('/drinks/<id>',),methods=["DELETE"])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error":"non found"}
    else:
        db.session.deltete(drink)
        db.session.commit()
        return {'message': 'delete'}
