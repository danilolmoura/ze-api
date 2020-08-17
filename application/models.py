from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point, MultiPolygon, Polygon

db = SQLAlchemy()

class Partner(db.Model):
    """Define schema for partner table
    """

    id = db.Column(
        db.Integer,
        primary_key=True,
        doc='id do parceiro')

    tradingName = db.Column(
        db.String(128),
        name='trading_name',
        nullable=False,
        doc='nome comercial')

    ownerName = db.Column(
        db.String(128),
        name='owner_name',
        nullable=False,
        doc='nome dono')

    document = db.Column(
        db.String(18),
        nullable=False,
        unique=True,
        doc='cnpj do usuário')

    address = db.Column(
        Geometry(geometry_type='POINT'),
        nullable=False,
        index=True,
        doc='endereço do parceiro')

    coverageArea = db.Column(
        Geometry(geometry_type='MULTIPOLYGON'),
        name='coverage_area',
        nullable=False,
        index=True,
        doc='cobertura do parceiro')

    @staticmethod
    def address_from_json(data):
        wkb_element = from_shape(
            Point(data['coordinates'][1], data['coordinates'][0]))

        return wkb_element

    @staticmethod
    def address_to_json(data):
        point = to_shape(data)

        return {
            'type': 'Point',
            'coordinates': [point.y, point.x]
        }

    @staticmethod
    def coverage_area_from_json(data):
        polygons = [Polygon(coords[0]) for coords in data['coordinates']]

        wkb_element = from_shape(MultiPolygon(polygons))

        return wkb_element

    @staticmethod
    def coverage_area_to_json(data):
        multipolygon = to_shape(data)

        return {
            'type': 'MultiPolygon',
            'coordinates': [
                [polygon.exterior.coords[:-1] for polygon in multipolygon]]
        }

    def to_json(self):
        return {
            'address': Partner.address_to_json(self.address),
            'coverageArea': Partner.coverage_area_to_json(self.coverageArea),
            'document': self.document,
            'ownerName': self.ownerName,
            'tradingName': self.tradingName,
            '$id': self.id
        }
