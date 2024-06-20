import os

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/sistem-pakar')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:@localhost:3306/sistem_pakar')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
