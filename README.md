# Wolt Delivery Order Price Calculator service (DOPC)
 
Task is to implement the Delivery Order Price Calculator service, or DOPC for short! DOPC is an imaginary backend service which is capable of calculating the total price and price breakdown of a delivery order. DOPC integrates with the Home Assignment API to fetch venue related data required to calculate the prices. The term venue refers to any kind of restaurant / shop / store that's in Wolt. Let's not make strict assumptions about the potential clients of DOPC: they might be other backend services, Wolt's consumer mobile apps, or even some third parties which integrate with Wolt.

sequenceDiagram
    box Users of our service
    participant Client
    end
    box Green You'll implement this
    participant DOPC
    end
    box Dependencies
    participant Home Assignment API
    end
    Client ->> DOPC: GET /api/v1/delivery-order-price
    par
        DOPC ->> Home Assignment API: GET /home-assignment-api/v1/venues/<venue slug>/static
        Home Assignment API -->> DOPC: 
    and
        DOPC ->> Home Assignment API: GET /home-assignment-api/v1/venues/<venue slug>/dynamic
        Home Assignment API -->> DOPC: 
    end
    DOPC -->> Client: Price information in the payload


