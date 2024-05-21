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

class Penyakit(db.Model):
    __tablename__ = 'penyakit'
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(10), nullable=False)
    nama = db.Column(db.String(100), nullable=False)

class Gejala(db.Model):
    __tablename__ = 'gejala'
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(10), nullable=False)
    nama = db.Column(db.String(100), nullable=False)

class Keputusan(db.Model):
    __tablename__ = 'keputusan_data'
    id = db.Column(db.Integer, primary_key=True)
    kode_penyakit = db.Column(db.String(10), nullable=False)
    kode_gejala = db.Column(db.String(255), nullable=False)  # Perubahan panjang kolom kode_gejala
    penyakit_id = db.Column(db.Integer, db.ForeignKey('penyakit.id'))
    gejala_id = db.Column(db.Integer, db.ForeignKey('gejala.id'))

class NilaiCFGejala(db.Model):
    __tablename__ = 'nilai_cf_gejala'
    id = db.Column(db.Integer, primary_key=True)
    penyakit_id = db.Column(db.Integer, db.ForeignKey('penyakit.id'), nullable=False)
    gejala_id = db.Column(db.Integer, db.ForeignKey('gejala.id'), nullable=False)
    nilai_cf = db.Column(db.Float, nullable=False)

    penyakit = db.relationship('Penyakit', backref=db.backref('nilai_cf_gejala', lazy=True))
    gejala = db.relationship('Gejala', backref=db.backref('nilai_cf_gejala', lazy=True))
