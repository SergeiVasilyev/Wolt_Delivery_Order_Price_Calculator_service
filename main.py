from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from services.delivery_calc import calculate_delivery_fee, calculate_distance, calculate_small_order_surcharge, calculate_total_price
from services.wolt_api import get_coordinates, get_dynamic_data
from error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
    type_error_handler
)



app = FastAPI()

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(TypeError, type_error_handler)


DELEVERY_ORDER_PRICE_API_URL = "/api/v1/delivery-order-price/"
HOME_ASSIGNMENT_API_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"


@app.get(DELEVERY_ORDER_PRICE_API_URL)
def read_item(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
    if cart_value < 0:
        raise HTTPException(status_code=400, detail="Invalid input parameters. Cart value cannot be negative.")
    if user_lat < -90 or user_lat > 90 or user_lon < -180 or user_lon > 180:
        raise HTTPException(status_code=400, detail="Invalid input parameters. Latitude must be between -90 and 90 and longitude must be between -180 and 180.")

    coordinates = get_coordinates({"venue_slug": venue_slug, "url": HOME_ASSIGNMENT_API_URL})
    dynamic_data = get_dynamic_data({"venue_slug": venue_slug, "url": HOME_ASSIGNMENT_API_URL})

    distance = calculate_distance(user_lat, user_lon, coordinates[1], coordinates[0])
    
    delivery_fee = calculate_delivery_fee(distance, dynamic_data)   
    small_order_surcharge = calculate_small_order_surcharge(cart_value, dynamic_data["order_minimum_no_surcharge"])
    total_price = calculate_total_price(cart_value, delivery_fee, small_order_surcharge)

    return {
        "total_price": total_price,
        "small_order_surcharge": small_order_surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": distance
        }
    }
