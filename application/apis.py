import datetime
import logging
import pdb

from flask_potion import fields, ModelResource
from flask_potion.routes import ItemRoute

from application.models import Partner

logger = logging.getLogger()

from geoalchemy2 import Geometry


class PartnerResource(ModelResource):
    class Meta:
        include_id = True
        model = Partner
        name = 'partner'

    class Schema:
        address = fields.Custom({})
        coverage_area = fields.Custom({})


def create_apis(api):
    api.add_resource(PartnerResource)
