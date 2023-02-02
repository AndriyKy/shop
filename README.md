# Shop
Web service for shop, which includes both user interface and API.

## Features
- Admin panel [ **admin/** ]
- Documentation [ **shop_api/doc/swagger/** ]
- List products (web page [ **shop_service/products/** ]) 
with searching by category and filtering by all columns
- Creating orders (through web page [ **shop_service/create_order/** ], 
jQuery web page [ **shop_service/create_order/jquery/** ] 
and API [ **shop_api/orders/** ])
- List orders (API  [ **shop_api/orders/** ])

## Installing using GitHub
Python 3 has to be already installed
```bash
git clone https://github.com/AndriyKy/shop.git
cd shop
python3 -m venv venv
sourve venv/bin/activate
pip install -r requirements.txt
````
- Copy **.env.sample** -> **.env** and populate with all required data

```bash
python3 manage.py collectstatic
python3 manage.py migrate
python3 manage.py runserver
```