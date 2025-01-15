import unittest
import sys
from pathlib import Path
from fastapi import HTTPException
from typeguard import TypeCheckError

sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.delivery_calc import (
    calculate_distance,
    calculate_small_order_surcharge,
    calculate_total_price,
    calculate_delivery_fee
)

class TestDeliveryCalc(unittest.TestCase):
    def test_calculate_distance(self):
        # Test with valid inputs
        lat1, lon1 = 52.5200, 13.4050  # Berlin, Germany
        lat2, lon2 = 48.8566, 2.3522  # Paris, France
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        self.assertGreater(distance, 0)
        self.assertAlmostEqual(distance, 877738.78, places=2)

        # Test with invalid inputs
        with self.assertRaises(TypeCheckError):
            calculate_distance('lat1', lon1, lat2, lon2)


    def test_calculate_delivery_fee(self):
        # Test with valid inputs
        distance = 200.0
        dynamic_data = {
            "distance_ranges": [
                {'min': 0, 'max': 500, 'a': 0, 'b': 0.0, 'flag': None},
                {'min': 500, 'max': 1000, 'a': 100, 'b': 0.0, 'flag': None},
                {'min': 1000, 'max': 1500, 'a': 200, 'b': 0.0, 'flag': None},
                {'min': 1500, 'max': 2000, 'a': 200, 'b': 1.0, 'flag': None},
                {'min': 2000, 'max': 0, 'a': 0, 'b': 0.0, 'flag': None}
            ],
            "base_price": 190
        }
        delivery_fee = calculate_delivery_fee(distance, dynamic_data)
        self.assertEqual(delivery_fee, 190)

        distance = 600.0
        delivery_fee = calculate_delivery_fee(distance, dynamic_data)
        self.assertEqual(delivery_fee, 290)

        distance = 1600
        delivery_fee = calculate_delivery_fee(distance, dynamic_data)
        self.assertEqual(delivery_fee, 550)

        # Test with invalid inputs
        distance = 2000
        with self.assertRaises(HTTPException):
            calculate_delivery_fee(distance, dynamic_data)

        with self.assertRaises(TypeCheckError):
            calculate_delivery_fee('distance', dynamic_data)


    def test_calculate_small_order_surcharge(self):
        # Test with valid inputs
        cart_value = 10
        order_minimum_no_surcharge = 20
        surcharge = calculate_small_order_surcharge(cart_value, order_minimum_no_surcharge)
        self.assertEqual(surcharge, 10)

        cart_value = 25
        order_minimum_no_surcharge = 20
        surcharge = calculate_small_order_surcharge(cart_value, order_minimum_no_surcharge)
        self.assertEqual(surcharge, 0)

        # Test with invalid inputs
        with self.assertRaises(TypeCheckError):
            calculate_small_order_surcharge('cart_value', order_minimum_no_surcharge)


    def test_calculate_total_price(self):
        # Test with valid inputs
        cart_value = 10
        delivery_fee = 5
        small_order_surcharge = 2
        total_price = calculate_total_price(cart_value, delivery_fee, small_order_surcharge)
        self.assertEqual(total_price, 17)

        # Test with invalid inputs
        with self.assertRaises(TypeCheckError):
            calculate_total_price('cart_value', delivery_fee, small_order_surcharge)





if __name__ == '__main__':
    unittest.main()