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
    kode_penyakit = db.Column(db.String(10), primary_key=True)  # Contoh panjang 10 karakter
    nama_penyakit = db.Column(db.String(255), nullable=False)  # Contoh panjang 255 karakter
    deskripsi = db.Column(db.String(255), nullable=False)  # Contoh panjang 255 karakter

class Gejala(db.Model):
    __tablename__ = 'gejala'
    kode_gejala = db.Column(db.String(10), primary_key=True)  # Contoh panjang 10 karakter
    nama_gejala = db.Column(db.String(255), nullable=False)  # Contoh panjang 255 karakter

class Aturan(db.Model):
    __tablename__ = 'aturan'
    id = db.Column(db.Integer, primary_key=True)
    kode_penyakit = db.Column(db.String(10), db.ForeignKey('penyakit.kode_penyakit'), nullable=False)
    kode_gejala = db.Column(db.String(10), db.ForeignKey('gejala.kode_gejala'), nullable=False)
    cf_value = db.Column(db.Float, nullable=False)

    penyakit = db.relationship('Penyakit', backref='aturan', lazy=True)  # Contoh pengaturan relasi
    gejala = db.relationship('Gejala', backref='aturan', lazy=True)  # Contoh pengaturan relasi
