import pdb

from flask_potion import fields, ModelResource
from flask_potion.routes import Route
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point, MultiPolygon

from application.models import Partner

class GeometrySerializer:
    @staticmethod
    def address_converter(data):
        wkb_element = from_shape(
            Point(data['coordinates'][1], data['coordinates'][0]))

        return wkb_element

    @staticmethod
    def address_formatter(data):
        point = to_shape(data)

        return {
            "type": "Point",
            "coordinates": [point.y, point.x]
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
        address = fields.Custom(
            {},
            converter=GeometrySerializer.address_converter,
            formatter=GeometrySerializer.address_formatter)

        coverage_area = fields.Custom(
            {},
            converter=GeometrySerializer.coverage_area_converter,
            formatter=GeometrySerializer.coverage_area_formatter)

    @Route.GET('/nearest')
    def nearest(
        self,
        lat: fields.Number(nullable=False),
        long: fields.Number(nullable=False)):
        """Find the nearest Partner given an specific position

        Args:
            lat  (Number): latitude of the given posi
            long (Number): Description

        Returns:
            dict: Representation of Parner found
        """
        point = Point(long, lat)

        partners = Partner.query.filter(
            Partner.coverage_area.ST_Contains(from_shape(point))).all()

        closer_partner = None
        max_distance = float('inf')
        if not partners:
            return closer_partner

        for partner in partners:
            partner_point = to_shape(partner.address)
            points_distance = point.distance(partner_point)

            if points_distance < max_distance:
                closer_partner = partner
                max_distance = points_distance

        return {
            '$id': closer_partner.id,
            'address': GeometrySerializer.address_formatter(
                closer_partner.address),
            'coverage_area': GeometrySerializer.coverage_area_formatter(
                closer_partner.coverage_area),
            'document': closer_partner.document,
            'owner_name': closer_partner.owner_name,
            'trading_name': closer_partner.trading_name
        }

def create_apis(api):
    api.add_resource(PartnerResource)
