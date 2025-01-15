import requests


def home_assignment_api(url: str, venue_slug: str = None, arg: str = None) -> dict:
    """
    Fetches data from the home assignment API.

    Args:
        url (str): The base URL of the API.
        venue_slug (str, optional): The venue identifier to be appended to the URL.
        arg (str, optional): Additional argument to be appended to the URL.

    Returns:
        dict: The JSON response from the API.

    Raises:
        Exception: If there is an error while fetching data from the API.
    """

    try:
        response = requests.get(f"{url}/{venue_slug}/{arg}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data: {e}")


def get_coordinates(data: dict) -> list[float]:
    """
    Gets coordinates from Wolt's Home Assignment API.

    :param data: Dict with "url" and "venue_slug" keys.
    :return: List of floats, length 2. The first element is the latitude, and the second is the longitude.
    :raises Exception: If the request fails, or if the response is not in the expected format.
    """
    data = home_assignment_api(**data, arg="static")

    try:
        coordinates: list[float] = data["venue_raw"]["location"]["coordinates"]
    except Exception as e:
        raise Exception(f"Error parsing data: {e}")

    return coordinates


def get_dynamic_data(data: dict) -> dict:
    """
    Gets dynamic data from Wolt's Home Assignment API.

    :param data: Dict with "url" and "venue_slug" keys.
    :return: Dict with "order_minimum_no_surcharge", "base_price", and "distance_ranges" keys.
    :raises Exception: If the request fails, or if the response is not in the expected format.
    """
    data = home_assignment_api(**data, arg="dynamic")

    try:
        order_minimum_no_surcharge: int = data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
        base_price: int = data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
        distance_ranges: list[dict] = data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
    except Exception as e:
        raise Exception(f"Error parsing data: {e}")

    return {
        "order_minimum_no_surcharge": order_minimum_no_surcharge,
        "base_price": base_price,
        "distance_ranges": distance_ranges
    }

