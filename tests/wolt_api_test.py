import unittest
import sys
from pathlib import Path
import unittest
from unittest.mock import patch, Mock
sys.path.append(str(Path(__file__).resolve().parent.parent))
from services.wolt_api import home_assignment_api, get_coordinates, get_dynamic_data


class TestWoltApi(unittest.TestCase):

    @patch('requests.get')
    def test_home_assignment_api(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'key': 'value'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = 'https://example.com'
        venue_slug = 'venue-slug'
        arg = 'arg'

        response = home_assignment_api(url, venue_slug, arg)

        # Successful case
        self.assertEqual(response, {'key': 'value'})
        mock_get.assert_called_once_with(f'{url}/{venue_slug}/{arg}')

        # Error case
        mock_response.raise_for_status.side_effect = Exception('Error')
        with self.assertRaises(Exception):
            home_assignment_api(url, venue_slug, arg)

    
    @patch('services.wolt_api.home_assignment_api')
    def test_get_coordinates(self, mock_home_assignment_api):
        mock_response = {'venue_raw': {'location': {'coordinates': [1.0, 2.0]}}}
        mock_home_assignment_api.return_value = mock_response

        data = {'url': 'https://example.com', 'venue_slug': 'venue-slug'}

        coordinates = get_coordinates(data)

        # Successful case
        self.assertEqual(coordinates, [1.0, 2.0])
        mock_home_assignment_api.assert_called_once_with(**data, arg='static')

        # Error case
        mock_response = {'venue_raw': {}}
        mock_home_assignment_api.return_value = mock_response

        with self.assertRaises(Exception):
            get_coordinates(data)


    @patch('services.wolt_api.home_assignment_api')
    def test_get_dynamic_data_success(self, mock_home_assignment_api):
        mock_response = {
            'venue_raw': {
                'delivery_specs': {
                    'order_minimum_no_surcharge': 10,
                    'delivery_pricing': {
                        'base_price': 5,
                        'distance_ranges': [{'min': 0, 'max': 10, 'a': 1, 'b': 2, 'flag': None}]
                    }
                }
            }
        }
        mock_home_assignment_api.return_value = mock_response

        data = {'url': 'https://example.com', 'venue_slug': 'venue-slug'}

        dynamic_data = get_dynamic_data(data)

        # Successful case
        control_values = {
            'order_minimum_no_surcharge': 10,
            'base_price': 5,
            'distance_ranges': [{'min': 0, 'max': 10, 'a': 1, 'b': 2, 'flag': None}]
        }
        self.assertEqual(dynamic_data, control_values)
        mock_home_assignment_api.assert_called_once_with(**data, arg='dynamic')

        # Error case
        mock_response = {'venue_raw': {}}
        mock_home_assignment_api.return_value = mock_response

        with self.assertRaises(Exception):
            get_dynamic_data(data)


if __name__ == '__main__':
    unittest.main()