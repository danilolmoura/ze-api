import json
import pdb

from application.models import Partner
from . import test_utils

class TestPartnerResource():
    url_partner = '/api/v1/partner'
    url_partner_item = '/api/v1/partner/{}'
    url_nearest = '/api/v1/partner/nearest'

    def test_create_partner_endpoint(self, test_client, session, teardown):
        def should_create_a_partner(test_client, session):
            trading_name = "Bar do Ze"
            owner_name = "Joao Silva"
            document = "04698149428"
            coverage_area = {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [-43.36556, -22.99669],
                            [-43.36539, -23.01928],
                            [-43.26583, -23.01802],
                            [-43.25724, -23.00649],
                            [-43.23355, -23.00127],
                            [-43.2381, -22.99716],
                            [-43.23866, -22.99649],
                            [-43.24063, -22.99756],
                        ]
                    ]
                ]
            }
            address = {
                "type": "Point",
                "coordinates": [-43.297337, -23.013538]
            }

            data = {
                "tradingName": trading_name,
                "ownerName": owner_name,
                "document": document,
                "coverageArea": coverage_area,
                "address": address
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            assert res.status_code == 200
            res_json = json.loads(res.data)

            assert res_json['tradingName'] == trading_name
            assert res_json['ownerName'] == owner_name
            assert res_json['document'] == document
            assert res_json['coverageArea'] == coverage_area
            assert res_json['address'] == address

        def should_raise_409_when_tries_to_creeate_a_partner_with_existing_document(test_client, session):
            common_document = '046981494281'

            trading_name = "Bar do Ze"
            owner_name = "Joao Silva"
            coverage_area = {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [-43.36556, -22.99669],
                            [-43.36539, -23.01928],
                            [-43.26583, -23.01802],
                            [-43.25724, -23.00649],
                            [-43.23355, -23.00127],
                            [-43.2381, -22.99716],
                            [-43.23866, -22.99649],
                            [-43.24063, -22.99756],
                        ]
                    ]
                ]
            }
            address = {
                "type": "Point",
                "coordinates": [-43.297337, -23.013538]
            }

            data = {
                "tradingName": trading_name,
                "ownerName": owner_name,
                "document": common_document,
                "coverageArea": coverage_area,
                "address": address
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            assert res.status_code == 200

            data = {
                "tradingName": trading_name,
                "ownerName": owner_name,
                "document": common_document,
                "coverageArea": coverage_area,
                "address": address
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            assert res.status_code == 409

        should_create_a_partner(test_client, session)
        should_raise_409_when_tries_to_creeate_a_partner_with_existing_document(test_client, session)

    def test_get_partner_endpoint(self, test_client, session, teardown):
        def should_return_partner_for_a_specified_id(test_client, session):
            data = {
                "tradingName": "Bar do Ze",
                "ownerName": "Joao Silva",
                "document": "04111111111",
                "coverageArea": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [-43.36556, -22.99669],
                                [-43.36539, -23.01928],
                                [-43.26583, -23.01802],
                                [-43.25724, -23.00649],
                                [-43.23355, -23.00127]
                            ]
                        ]
                    ]
                },
                "address": {
                "type": "Point",
                "coordinates": [-43.297337, -23.013538]
                }
            }

            # Create a partner
            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            assert res.status_code == 200
            partner_id = json.loads(res.data)['$id']


            # get partner by id
            res = test_client.get(
                self.url_partner_item.format(partner_id),
                headers=test_utils.get_headers())

            assert res.status_code == 200
            assert partner_id == json.loads(res.data)['$id']

        should_return_partner_for_a_specified_id(test_client, session)

    def test_search_nearest_partner_endpoint(self, test_client, session, teardown):
        def should_return_the_nearest_partner(test_client, session):
            data = {
                "tradingName": "Bar do Ze",
                "ownerName": "Joao Silva",
                "document": "04111111111",
                "coverageArea": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [-43.36556, -22.99669],
                                [-43.36539, -23.01928],
                                [-43.26583, -23.01802],
                                [-43.25724, -23.00649],
                                [-43.23355, -23.00127]
                            ]
                        ]
                    ]
                },
                "address": {
                "type": "Point",
                "coordinates": [-43.297337, -23.013538]
                }
            }

            # Create a partner
            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            partner_id = json.loads(res.data)['$id']
            data = {
                'long': -43.311675, 'lat': -23.010202
            }

            res = test_client.get(
                self.url_nearest,
                data=json.dumps(data),
                headers=test_utils.get_headers())

            assert {
                '$id': partner_id,
                'address': {
                    'coordinates': [-43.297337, -23.013538],
                    'type': 'Point'
                },
                'coverageArea': {
                    'coordinates': [
                        [
                            [
                                [-43.36556, -22.99669],
                                [-43.36539, -23.01928],
                                [-43.26583, -23.01802],
                                [-43.25724, -23.00649],
                                [-43.23355, -23.00127]
                            ]
                        ]
                    ],
                    'type': 'MultiPolygon'
                },
                'document': '04111111111',
                'ownerName': 'Joao Silva',
                'tradingName': 'Bar do Ze'
            } == json.loads(res.data)

        should_return_the_nearest_partner(test_client, session)
