from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import random
##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/all',methods=["GET"])
def all():
    cafes=Cafe.query.all()
    print(cafes)
    list={}
    for cafe in cafes:
        data={
            cafe.id:{
                'name':cafe.name,
                'img_url':cafe.img_url,
                'map_url':cafe.map_url,
                'location':cafe.location,
                'has_sockets':cafe.has_sockets,
                'has_toilet':cafe.has_toilet,
                'has_wifi':cafe.has_wifi,
                'can_take_calls':cafe.can_take_calls,
                'seats':cafe.seats,
                'coffee_price':cafe.coffee_price
            }
            
        }
        list.update(data)

    return jsonify(list)

@app.route('/update-price',methods=["PATCH"])
def update_price():
    cafeid=request.args.get('id')
    price=request.args.get('price')
    
    try:
        cafe=Cafe.query.filter_by(id=int(cafeid)).first()
        cafe.coffee_price=price
        db.session.commit()
        message={
        'response':{
            'success':'Successfully added the new cafe.'
        }
    }
        return jsonify(message),200
    except:
        message={
        'response':{
            'error':'Check your parameters again carefully.'
        }
        }
        return jsonify(message),404
api_key="TopSecretApiKey"   

@app.route('/report-closed',methods=["DELETE"])
def delete():
    try:
        cafeid=request.args.get('id')
        key=request.args.get('api_key','None')
        cafe=Cafe.query.get(cafeid)
        if key!=api_key:
            message={
            'response':{
                'error':'You are not allowed because the Api Key you provided is wrong'
            }
            }
            return jsonify(message)
        else:
            
            db.session.delete(cafe)
            db.session.commit()
            message={
            'response':{
                'success':'Task completed successfully'
            }
            }
            return jsonify(message)
       
    except:
        message={
            'error':'The id parameter is not right. Please check it again.'
        }    
     
        return jsonify(message),404


@app.route('/add',methods=["POST"])
def add_cafe():
    name=request.args.get('name')
    map_url=request.args.get('map_url','NONE')
    img_url=request.args.get('img_url','NONE')
    location=request.args.get('location','NONE')
    has_wifi=request.args.get('has_wifi',0)
    has_toilet=request.args.get('has_toilet',0)
    has_sockets=request.args.get('has_sockets',0)
    can_take_calls=request.args.get('can_take_calls',0)
    seats=request.args.get('seats','NONE')
    coffee_price=request.args.get('coffee_price','NONE')
    cafe=Cafe(name=name,map_url=map_url,img_url=img_url,location=location,has_sockets=int(has_sockets),has_toilet=int(has_toilet),has_wifi=int(has_wifi),can_take_calls=int(can_take_calls),seats=seats,
        coffee_price=coffee_price)
    db.session.add(cafe)
    db.session.commit()    
    message={
        'response':{
            'success':'Successfully added the new cafe.'
        }
    }
    return jsonify(message)
@app.route('/search',methods=["GET"])
def search_by_location():
    location=request.args.get('loc',None)
    print(location)
    cafes=Cafe.query.filter_by(location=f"{location}").all()
    list={}

    for cafe in cafes:
        
         data={
            cafe.id:{
                'name':cafe.name,
                'img_url':cafe.img_url,
                'map_url':cafe.map_url,
                'location':cafe.location,
                'has_sockets':cafe.has_sockets,
                'has_toilet':cafe.has_toilet,
                'has_wifi':cafe.has_wifi,
                'can_take_calls':cafe.can_take_calls,
                'seats':cafe.seats,
                'coffee_price':cafe.coffee_price
            }}
         list.update(data)
    statement={
        'error':{
        'Not Found':'Sorry, we dont have a cafe at that location ' 
        }
    }
    if len(list)==0:
        return jsonify(statement)
    else:
        return jsonify(list)

@app.route('/random',methods=["GET"])
def random_cafe():
        cafe=Cafe.query.all()
        random_cafe_info=random.choice(cafe)
        return jsonify(name=random_cafe_info.name,map_url=random_cafe_info.map_url,img_url=random_cafe_info.img_url,location=random_cafe_info.location,has_sockets=random_cafe_info.has_sockets,has_toilet=random_cafe_info.has_toilet,has_wifi=random_cafe_info.has_wifi,can_take_calls=random_cafe_info.can_take_calls,seats=random_cafe_info.seats,
        coffee_price=random_cafe_info.coffee_price
        
        )
## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
