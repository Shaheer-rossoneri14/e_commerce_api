# e_commerce_api
**E-commerce API using Django REST Framework, PostgreSQL and Redis.**

# Features
- User registration and login
- Product list, creation, retrieval, update, and deletion (CRUD)
- Placing an order, viewing an order, updating the status of an order, and canceling an order

# Database Schema:
## User:
- id: Auto-incrementing unique identifier
- username: Unique username
- password: Hashed password
- email: Unique email
- date_joined: Date and time the user joined
## Product:
- id: Auto-incrementing unique identifier
- name: Name of the product
- description: Description of the product
- price: Price of the product
- date_created: Date and time the product was added
- date_updated: Date and time the product was last updated
## Order:
- id: Auto-incrementing unique identifier
- user_id: Foreign Key linking to the User that placed the order
- date_placed: Date and time the order was placed
- status: Current status of the order (e.g., placed, shipped, delivered, cancelled)
## OrderItem:
- id: Auto-incrementing unique identifier
- order_id: Foreign Key linking to the Order
- product_id: Foreign Key linking to the Product
- quantity: Number of that product in the order

# API Endpoints:
## User:
- POST /api/register: Register a new user
- POST /api/login: Log in an existing user
## Product:
- POST /api/products: Create a new product
- GET /api/products: Retrieve all products
- GET /api/products/{id}: Retrieve a single product
- PUT /api/products/{id}: Update a single product
- DELETE /api/products/{id}: Delete a single product
## Order:
- POST /api/orders: Place a new order
- GET /api/orders: Retrieve all orders for the logged-in user
- GET /api/orders/{id}: Retrieve a single order for the logged-in user
- PUT /api/orders/{id}: Update the status of an order
- DELETE /api/orders/{id}: Cancel an order
