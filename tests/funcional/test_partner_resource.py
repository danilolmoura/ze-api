import json
import pdb

from application.models import Partner
from . import test_utils

class TestPartnerResource():
    url_partner = '/api/v1/partner'
    url_partner_item = '/api/v1/partner/{}'
    url_nearest_partner = '/api/v1/partner/{}/nearest'

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
                            [
                                38.56586,
                                3.85041
                            ],
                            [
                                38.49599,
                                3.87361
                            ],
                            [
                                38.45033,
                                3.90358
                            ],
                            [
                                38.42304,
                                3.90273
                            ],
                            [
                                38.37892,
                                3.88971
                            ],
                            [
                                38.35566,
                                3.8844
                            ],
                            [
                                38.39557,
                                3.82497
                            ],
                            [
                                38.41531,
                                3.80133
                            ],
                            [
                                38.42771,
                                3.76754
                            ],
                            [
                                38.44251,
                                3.75054
                            ],
                            [
                                38.45672,
                                3.75024
                            ],
                            [
                                38.46562,
                                3.74746
                            ],
                            [
                                38.46525,
                                3.74657
                            ],
                            [
                                38.46616,
                                3.74458
                            ],
                            [
                                38.46507,
                                3.74083
                            ],
                            [
                                38.47256,
                                3.73743
                            ],
                            [
                                38.47844,
                                3.72759
                            ],
                            [
                                38.49002,
                                3.72476
                            ],
                            [
                                38.49573,
                                3.72254
                            ],
                            [
                                38.51226,
                                3.71384
                            ],
                            [
                                38.51736,
                                3.74292
                            ],
                            [
                                38.52517,
                                3.7681
                            ],
                            [
                                38.53095,
                                3.78294
                            ],
                            [
                                38.53415,
                                3.79124
                            ],
                            [
                                38.5412,
                                3.79573
                            ],
                            [
                                38.55148,
                                3.80326
                            ],
                            [
                                38.55796,
                                3.82
                            ],
                            [
                                38.5656,
                                3.84839
                            ]
                        ]
                    ]
                ]
            }
            address = {
                "type": "Point",
                "coordinates": [
                    -38.495586,
                    -3.809936
                ]
            }

            data = {
                "trading_name": trading_name,
                "owner_name": owner_name,
                "document": document,
                "coverage_area": coverage_area,
                "address": address
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            assert res.status_code == 200
            res_json = json.loads(res.data)

            assert res_json['trading_name'] == trading_name
            assert res_json['owner_name'] == owner_name
            assert res_json['document'] == document
            assert res_json['coverage_area'] == coverage_area
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
                            [
                                38.56586,
                                3.85041
                            ],
                            [
                                38.49599,
                                3.87361
                            ],
                            [
                                38.45033,
                                3.90358
                            ],
                            [
                                38.42304,
                                3.90273
                            ],
                            [
                                38.37892,
                                3.88971
                            ],
                            [
                                38.35566,
                                3.8844
                            ],
                            [
                                38.39557,
                                3.82497
                            ],
                            [
                                38.41531,
                                3.80133
                            ],
                            [
                                38.42771,
                                3.76754
                            ],
                            [
                                38.44251,
                                3.75054
                            ],
                            [
                                38.45672,
                                3.75024
                            ],
                            [
                                38.46562,
                                3.74746
                            ],
                            [
                                38.46525,
                                3.74657
                            ],
                            [
                                38.46616,
                                3.74458
                            ],
                            [
                                38.46507,
                                3.74083
                            ],
                            [
                                38.47256,
                                3.73743
                            ],
                            [
                                38.47844,
                                3.72759
                            ],
                            [
                                38.49002,
                                3.72476
                            ],
                            [
                                38.49573,
                                3.72254
                            ],
                            [
                                38.51226,
                                3.71384
                            ],
                            [
                                38.51736,
                                3.74292
                            ],
                            [
                                38.52517,
                                3.7681
                            ],
                            [
                                38.53095,
                                3.78294
                            ],
                            [
                                38.53415,
                                3.79124
                            ],
                            [
                                38.5412,
                                3.79573
                            ],
                            [
                                38.55148,
                                3.80326
                            ],
                            [
                                38.55796,
                                3.82
                            ],
                            [
                                38.5656,
                                3.84839
                            ],
                            [
                                38.56586,
                                3.85041
                            ]
                        ]
                    ]
                ]
            }
            address = {
                "type": "Point",
                "coordinates": [
                    -38.495586,
                    -3.809936
                ]
            }

            data = {
                "trading_name": trading_name,
                "owner_name": owner_name,
                "document": common_document,
                "coverage_area": coverage_area,
                "address": address
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            assert res.status_code == 200

            data = {
                "trading_name": trading_name,
                "owner_name": owner_name,
                "document": common_document,
                "coverage_area": coverage_area,
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
                "trading_name": "Bar do Ze",
                "owner_name": "Joao Silva",
                "document": "04111111111",
                "coverage_area": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [
                                    38.56586,
                                    3.85041
                                ],
                                [
                                    38.49599,
                                    3.87361
                                ],
                                [
                                    38.45033,
                                    3.90358
                                ],
                                [
                                    38.56586,
                                    3.85041
                                ]
                            ]
                        ]
                    ]
                },
                "address": {
                "type": "Point",
                "coordinates": [
                        -38.495586,
                        -3.809936
                    ]
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
