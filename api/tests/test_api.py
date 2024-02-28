import requests
import environ
import unittest

import logging


class TraverseMenuLinksTestCase(unittest.TestCase):

    def setUp(self):

        # Set up data for testing
        self.env = environ.Env()
        self.token = self.env('API_AUTH_TOKEN', None)
        self.api_url = self.env('API_URL', None)
        self.headers = {
            'Authorization': 'Token ' + self.token,
            'Content-Type': 'application/json'
        }

        logging.basicConfig(level=logging.INFO) # Sets the level to show INFO messages

    def test_env(self):

        self.assertIsNotNone(self.token)
        self.assertIsNotNone(self.api_url)

    def test_catalog_response(self):

        response = requests.get(f'{self.api_url}/catalog', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_catalog_menu_lists(self):

        self.traverse_from_starting_point('/catalog')

    def convert_url(self, path : str) -> str:

        #logging.info(f'Converting for {path}')
        items_list = path.split('/')
        items_list = [x for x in items_list if x not in ['list', 'product', '', '/']]
        #logging.info(f'Converted {path} to {items_list[0]}')

        return  '/' + items_list[0]

    def traverse_from_starting_point(self, endpoint_path: str) -> None:
        logging.info(f'Attempting to reach {self.api_url + endpoint_path}')

        response = requests.get(self.api_url + endpoint_path, headers=self.headers)
        response_body: dict = response.json()

        if response.status_code == 404:
            raise ValueError(f'A problem with endpoint: {endpoint_path}, it returned error 404')

        body = response_body.get('body')
        is_product = 'images' in body.keys()

        if is_product:
            logging.info(f'This endpoint ({self.api_url + endpoint_path}) returns a product record for {body.get('name', None)}')
            return

        for record in body.get('records', []):
            endpoint_path = self.convert_url(record.get('url', None))

            if 'https' not in endpoint_path:
                self.traverse_from_starting_point(endpoint_path)


class TraverseDropDownLinksTestCase(unittest.TestCase):

    def setUp(self):

        # Set up data for testing
        self.env = environ.Env()
        self.token = self.env('API_AUTH_TOKEN', None)
        self.api_url = self.env('API_URL', None)
        self.site_url = self.env('SITE_URL', None)
        self.headers = {
            'Authorization': 'Token ' + self.token,
            'Content-Type': 'application/json'
        }

        logging.basicConfig(level=logging.INFO) # Sets the level to show INFO messages

    def test_drop_down_response(self):

        response = requests.get(f'https://api.bddw.com/api/drop-down-menu', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_drop_down_menu_links(self):

        response = requests.get(f'https://api.bddw.com/api/drop-down-menu', headers=self.headers)
        response_body : dict = response.json()
        records : list = response_body['body']

        self.traverse_drop_down_menu(records)

    def traverse_drop_down_menu(self, records :list ):

        for record in records:

            record_url = record.get('url')
            logging.info(f'Testing record {record.get('name')} at {record_url}')

            if record_url.startswith('http'): ## dont bother
                return

            response = requests.get(f'{self.site_url}{record_url}', headers=self.headers)

            if response.status_code == 404:
                raise ValueError(f'Issue with drop down menu record, {record.get('name', 'Undefined record')}')

            else:

                if record.get('children', []) != []:
                    for child in record.get('children'):
                        self.traverse_drop_down_menu(child)


# {
#     "body": [
#         {
#             "url": "/list/upholstery/",
#             "name": "UPHOLSTERY",
#             "order": 10,
#             "children": [
#                 [
#                     {
#                         "url": "/list/sofas-collection",
#                         "name": "sofas",
#                         "order": "1",
#                         "children": []
