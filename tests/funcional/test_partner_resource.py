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
            # create partner that covers the point
            partner1 = {
                'address': {'coordinates': [-46.693768, -23.569365], 'type': 'Point'},
                'coverageArea': {
                    'coordinates': [[[[-46.76338, -23.53597], [-46.7311, -23.60489], [-46.70055, -23.61936], [-46.6842, -23.63009], [-46.6766, -23.63894], [-46.66641, -23.62915], [-46.66131, -23.62771], [-46.66186, -23.6196], [-46.6595, -23.61805], [-46.6508, -23.62341], [-46.64678, -23.62989], [-46.62982, -23.62927], [-46.62673, -23.61484], [-46.62811, -23.60982], [-46.6209, -23.59442], [-46.61515, -23.58345], [-46.6094, -23.57719], [-46.60764, -23.57397], [-46.60785, -23.56925], [-46.61397, -23.55929], [-46.62352, -23.55578], [-46.62871, -23.54404], [-46.62485, -23.52008], [-46.6778, -23.51402], [-46.68331, -23.51027], [-46.69636, -23.50809], [-46.71939, -23.50878], [-46.73314, -23.50409], [-46.75288, -23.4986], [-46.751, -23.51262]]]],
                    'type': 'MultiPolygon'
                },
                'document': '10.144.318/0001-08',
                'ownerName': 'Messi Pele',
                'tradingName': 'Adega do Joao'
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(partner1))

            # create other partner that covers the point
            # this one has the closest address
            partner2 = {
                'address': {'coordinates': [-46.689537, -23.560505], 'type': 'Point'},
                'coverageArea': {
                    'coordinates': [[[[-46.71746, -23.50814], [-46.72013, -23.50895], [-46.72331, -23.51276], [-46.7314, -23.51754], [-46.73517, -23.51802], [-46.74327, -23.51768], [-46.74558, -23.51865], [-46.74741, -23.52103], [-46.74988, -23.53096], [-46.7592, -23.52901], [-46.76383, -23.53423], [-46.76237, -23.53981], [-46.76265, -23.54499], [-46.76267, -23.54638], [-46.7665, -23.55032], [-46.76728, -23.55305], [-46.76578, -23.55804], [-46.76816, -23.55888], [-46.76984, -23.56], [-46.76898, -23.56319], [-46.76966, -23.56418], [-46.7709, -23.56438], [-46.77316, -23.5681], [-46.77244, -23.57034], [-46.7714, -23.571], [-46.77143, -23.57167], [-46.77334, -23.57443], [-46.77279, -23.57545], [-46.76582, -23.57661], [-46.77349, -23.58309], [-46.77057, -23.58317], [-46.76609, -23.5851], [-46.75923, -23.58626], [-46.75543, -23.5866], [-46.75637, -23.58853], [-46.75561, -23.59194], [-46.75383, -23.59133], [-46.74959, -23.59246], [-46.74921, -23.59576], [-46.74612, -23.59584], [-46.74738, -23.59764], [-46.74717, -23.59881], [-46.74908, -23.60437], [-46.75149, -23.6076], [-46.75246, -23.61047], [-46.75421, -23.61157], [-46.75866, -23.61809], [-46.7576, -23.62094], [-46.75616, -23.62263], [-46.75379, -23.624], [-46.7503, -23.62325], [-46.74992, -23.62368], [-46.75031, -23.62517], [-46.75172, -23.62673], [-46.7525, -23.62978], [-46.75181, -23.62961], [-46.75082, -23.63027], [-46.75152, -23.63161], [-46.75113, -23.63374], [-46.75316, -23.63496], [-46.75224, -23.63644], [-46.7508, -23.63674], [-46.74995, -23.63873], [-46.74885, -23.64001], [-46.74658, -23.64041], [-46.7398, -23.63817], [-46.73826, -23.6387], [-46.73671, -23.6423], [-46.7344, -23.64412], [-46.72789, -23.64492], [-46.71969, -23.65622], [-46.71228, -23.66182], [-46.71025, -23.66499], [-46.70431, -23.66086], [-46.70115, -23.65989], [-46.69244, -23.65575], [-46.68614, -23.65145], [-46.68205, -23.6522], [-46.67993, -23.65366], [-46.67227, -23.64407], [-46.67632, -23.64046], [-46.67728, -23.6366], [-46.68411, -23.63027], [-46.68516, -23.62789], [-46.68716, -23.6263], [-46.67834, -23.61362], [-46.67643, -23.6088], [-46.67014, -23.58382], [-46.67124, -23.57699], [-46.66195, -23.57038], [-46.65726, -23.56554], [-46.65586, -23.5619], [-46.65284, -23.55795], [-46.64905, -23.55543], [-46.64626, -23.55169], [-46.64571, -23.55409], [-46.6435, -23.55535], [-46.6358, -23.55661], [-46.62804, -23.55614], [-46.62566, -23.55299], [-46.62827, -23.54755], [-46.62891, -23.54329], [-46.62495, -23.53419], [-46.6251, -23.51908], [-46.64203, -23.51853], [-46.67793, -23.51396], [-46.68353, -23.51034], [-46.69496, -23.50818], [-46.70711, -23.50875]]]],
                    'type': 'MultiPolygon'
                },
                'document': '15.127.213/0001-56',
                'ownerName': 'Daniel Henrique',
                'tradingName': 'SOS Cerveja'
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(partner2))

            partner2_id = json.loads(res.data)['$id']

            # finds the closest partner that covers the point
            data = {
                'long': -46.665700, 'lat': -23.556671
            }

            res = test_client.get(
                self.url_nearest,
                data=json.dumps(data),
                headers=test_utils.get_headers())

            # confirm that partner2 is the nearest one
            partner2['$id'] = partner2_id
            assert partner2 == json.loads(res.data)

        def should_return_null_if_theres_no_partner_that_covers_the_point(test_client, session):
            data = {
                "tradingName": "Bar do Ze",
                "ownerName": "Joao Silva",
                "document": '10.144.318/0002-08',
                "coverageArea": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [[[30, 20], [45, 40], [10, 40], [30, 20]]], 
                        [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
                    ]
                },
                "address": {
                    "type": "Point",
                    "coordinates": [-43.297337, -23.013538]
                }
            }

            res = test_client.post(
                self.url_partner,
                headers=test_utils.get_headers(),
                data=json.dumps(data))

            assert res.status_code == 200

            data = {
                'long': -10, 'lat': -15
            }

            res = test_client.get(
                self.url_nearest,
                data=json.dumps(data),
                headers=test_utils.get_headers())

            assert json.loads(res.data) == None

        should_return_the_nearest_partner(test_client, session)
        should_return_null_if_theres_no_partner_that_covers_the_point(test_client, session)
