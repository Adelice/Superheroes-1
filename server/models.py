from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Hero {self.id}>'

  
    def to_dict(self, include_powers=False):
        data = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
        if include_powers:
            data['hero_powers'] = [hero_power.to_simple_dict() for hero_power in self.hero_powers]
        return data


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Power {self.id}>'

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be at least 20 characters")
        return description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description 
        }
        
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    def __repr__(self):
        return f'<HeroPower {self.id}>'

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of 'Strong', 'Weak', 'Average'")
        return strength

    def to_dict(self, exclude_hero=False, exclude_power=False):
        data = {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id
        }
        if not exclude_hero:
            data['hero'] = self.hero.to_simple_dict()
        if not exclude_power:
            data['power'] = self.power.to_simple_dict()
        return data

    def to_simple_dict(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id
        }
