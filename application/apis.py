import pdb

from flask_potion import fields, ModelResource
from flask_potion.routes import Route
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point

from application.models import Partner

class PartnerResource(ModelResource):
    class Meta:
        include_id = True
        model = Partner
        name = 'partner'

    class Schema:
        address = fields.Custom(
            {},
            converter=Partner.address_from_json,
            formatter=Partner.address_to_json)

        coverageArea = fields.Custom(
            {},
            converter=Partner.coverage_area_from_json,
            formatter=Partner.coverage_area_to_json)

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
            Partner.coverageArea.ST_Contains(from_shape(point))).all()

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

        return partner.to_json()

def create_apis(api):
    api.add_resource(PartnerResource)
