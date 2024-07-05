#!/usr/bin/env python3

from flask import Flask, request, make_response,jsonify,abort 
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict(include_powers=True)), 200
    return jsonify({'error': 'Hero not found'}), 404
@app.route('/powers', methods=['GET'])
def get_powers():
    powers= Power.query.all()
    powers_list=[power.to_dict() for power in powers]

    return jsonify(powers_list)
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power=Power.query.get(id)

    if power:
        return jsonify(power.to_dict()), 200
    return jsonify({'error': 'Power not found'}), 404
@app.route('/powers/<int:id>',methods=['PATCH'])
def update_power(id):
    power=Power.query.get(id)
    if not power:
        return jsonify({'error':'Power not found'}),404
    try:
        data= request.get_json()
        new_description=data.get('description')
        if not new_description or len(new_description)<20:
            return jsonify({'error':'Descritption must be at least 20 characters'})
        power.description= new_description
        db.session.commit()

        return jsonify({'message':'Power updated successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
    finally:
        db.session.close()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
