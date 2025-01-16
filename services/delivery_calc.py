import math
from fastapi import HTTPException
from typeguard import typechecked


@typechecked
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:    
    """
    Calculates the great-circle distance between two points on the Earth's surface.

    This function uses the Haversine formula to calculate the distance between
    two geographical points specified by their latitude and longitude in decimal 
    degrees. See https://en.wikipedia.org/wiki/Haversine_formula

    :param lat1: Latitude of the first point in decimal degrees.
    :param lon1: Longitude of the first point in decimal degrees.
    :param lat2: Latitude of the second point in decimal degrees.
    :param lon2: Longitude of the second point in decimal degrees.
    :return: The distance between the two points in kilometers.
    """

    R = 6373000.0  # Earth's radius in meters

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sqrt((1 - math.cos(dlat) + math.cos(lat1) * math.cos(lat2) * (1 - math.cos(dlon))) / 2)
    distance = 2 * R * math.asin(a)

    return round(distance)
    
@typechecked
def calculate_delivery_fee(distance: float, dynamic_data: dict) -> int:
    """
    Calculates the delivery fee based on the distance and dynamic data.

    :param distance: The distance in kilometers.
    :param dynamic_data: A dictionary containing the dynamic data.
    :return: The delivery fee.
    """

    if distance >= dynamic_data["distance_ranges"][-1]["min"]:
        raise HTTPException(status_code=400, detail=f"Distance exceeds maximum limit of {dynamic_data['distance_ranges'][-1]['min']} meters")

    a, b = 0, 0
    for n in dynamic_data["distance_ranges"][:-1]:
        if n["min"] <= distance < n["max"]:
            a, b = n["a"], n["b"]
            break

    delivery_fee = round(dynamic_data["base_price"] + a + b * distance / 10)

    return delivery_fee
    

@typechecked
def calculate_small_order_surcharge(cart_value: int, order_minimum_no_surcharge: int) -> int:
    """
    Calculates the small order surcharge based on the cart value.

    If the cart value is less than the order minimum required to avoid a surcharge,
    this function returns the difference as the small order surcharge. If the cart
    value is greater than or equal to the order minimum, the surcharge is zero.

    :param cart_value: The total value of the cart.
    :param order_minimum_no_surcharge: The minimum order value required to avoid a surcharge.
    :return: The small order surcharge.
    """

    small_order_surcharge = order_minimum_no_surcharge - cart_value
    if small_order_surcharge < 0:
        return 0
    return small_order_surcharge


@typechecked
def calculate_total_price(cart_value: int, delivery_fee: int, small_order_surcharge: int) -> int:
    """
    Calculates the total price based on the cart value, delivery fee, and small order surcharge.

    :param cart_value: The total value of the cart.
    :param delivery_fee: The delivery fee.
    :param small_order_surcharge: The small order surcharge.
    :return: The total price.
    """
    return cart_value + delivery_fee + small_order_surcharge
