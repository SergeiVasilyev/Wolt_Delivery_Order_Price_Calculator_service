# Wolt Delivery Order Price Calculator service (DOPC)
 
This is my implementation of the Delivery Order Price Calculator service for the Wolt company.

Here is the full description of the project:  
https://github.com/woltapp/backend-internship-2025?tab=readme-ov-file

# Project deployed on the Render Cloud Platform
https://wolt-delivery-order-price-calculator.onrender.com/api/v1/delivery-order-price/?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.175&user_lon=24.93087

*Sometimes the Render service takes some time to wake up and start the program.*

# Tech Stack
- Python
- FastApi

# Install and Run using Docker

Create build  
```
docker build -t wolt_dopc .
```

Run build  
```
docker run -d -p 8000:8000 wolt_dopc
```


# Make request
http://127.0.0.1:8000/api/v1/delivery-order-price/?venue_slug=home-assignment-venue-helsinki&cart_value=500&user_lat=60.180&user_lon=24.93087


### Specification

The DOPC service should provide a single endpoint: GET /api/v1/delivery-order-price, which takes the following as query parameters (all are required):

- ``venue_slug`` (string): The unique identifier (slug) for the venue from which the delivery order will be placed
- ``cart_value`` (integer): The total value of the items in the shopping cart
- ``user_lat`` (number with decimal point): The latitude of the user's location
- ``user_lon`` (number with decimal point): The longitude of the user's location

The endpoint return a JSON response in the following format:
```JSON
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```

Errors format:
```JSON
{
  "success": false,
  "errors": [
    {
      "code": "HTTP_ERROR",
      "message": "Distance exceeds maximum limit of 2000 meters"
    }
  ]
}

```

# Stop Docker container

Shaw all running containers  
```
docker ps
```

Stop container   
```
docker stop <container_name_or_id>
```


# Manual instalation 

Install virtual environment
```
python -m venv venv
```

Install Dependencies
```
pip install -r requirements.txt
```

Run
```
fastapi dev main.py --port 8001
```
