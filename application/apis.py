import datetime
import logging
import pdb

from flask_potion import fields, ModelResource
from flask_potion.routes import ItemRoute
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point, MultiPolygon

from application.models import Partner

logger = logging.getLogger()

class GeometrySerializer:
    @staticmethod
    def address_converter(data):
        wkb_element = from_shape(
            Point(data['coordinates'][0], data['coordinates'][1]))
        return wkb_element

    @staticmethod
    def address_formatter(data):
        point = to_shape(data)

        return {
            "type": "Point",
            "coordinates": [
               point.x,
               point.y
            ]
        }

    @staticmethod
    def coverage_area_converter(data):
        wkb_element = from_shape(
            MultiPolygon([[data['coordinates'][0][0], []]]))
        return wkb_element

    @staticmethod
    def coverage_area_formatter(data):
        multipolygon = to_shape(data)

        return {
            "type": "MultiPolygon",
            "coordinates": [
                [polygon.exterior.coords[:-1] for polygon in multipolygon]]
        }


class PartnerResource(ModelResource):
    class Meta:
        include_id = True
        model = Partner
        name = 'partner'

    class Schema:
        pass

def create_apis(api):
    api.add_resource(PartnerResource)
