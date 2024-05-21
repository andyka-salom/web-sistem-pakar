from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Personality(db.Model):
    __tablename__ = 'personalities'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

class Trait(db.Model):
    __tablename__ = 'traits'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

class ExpertSystem(db.Model):
    __tablename__ = 'expert_system'
    id = db.Column(db.Integer, primary_key=True)
    personality_id = db.Column(db.Integer, db.ForeignKey('personalities.id'), nullable=False)
    trait_id = db.Column(db.Integer, db.ForeignKey('traits.id'), nullable=False)
