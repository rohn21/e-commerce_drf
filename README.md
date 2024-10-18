
# E-commerce API using Python, Django

This APIs includes building an `e-commerce api` using `Django REST Framework` to manage Customers, Products, and Orders.

This webapp can handle multiple customers along with multiple orders using table relations and keys. Each orders can contain multiple products with several quantities.

It also includes some `custom serializers validations` related to the API e.g. unique products, limited products,orders weight.
To handle orders, `nested serializers` used for better code optimization and readability.

Additionally, it contains url filters for example orders based on customer_name and product_name.


## Installation

clone the repo

```bash
  git clone https://github.com/rohn21/e-commerce_drf.git
```

```bash
  cd e_commerce_api
```


## Usage/Examples
Database migration
```
python manage.py makemigrations

python manage.py migrate
```

To run the server
```
python manage.py runserver
```