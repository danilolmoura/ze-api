from geoalchemy2 import Geometry
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Partner(db.Model):
    """Define schema for partner table
    """

    id = db.Column(
        db.Integer,
        primary_key=True,
        doc='id do parceiro')

    trading_name = db.Column(
        db.String(128),
        nullable=False,
        doc='nome comercial')

    owner_name = db.Column(
        db.String(128),
        nullable=False,
        doc='nome dono')

    document = db.Column(
        db.String(18),
        nullable=False,
        unique=True,
        doc='cnpj do usuário')

    address = db.Column(
        Geometry(geometry_type='POINT'),
        nullable=True,
        index=True,
        doc='endereço do parceiro')

    coverage_area = db.Column(
        Geometry(geometry_type='MULTIPOLYGON'),
        nullable=True,
        index=True,
        doc='cobertura do parceiro')
