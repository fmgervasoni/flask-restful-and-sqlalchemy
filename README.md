# REST APIs with Flask and Python

Project from course https://udemy.com/course/rest-api-flask-and-python/

## Requirements

- Python 3.10
- Pip
- Virtualenv (optional)

## Installation

If you decide to run it in a virtual environment, perform the following steps within a virtual environment

```bash
pip3 install -r requirements.txt
```

Run the program

To run the program you need to go to the root directory and execute:

```bash
python3 app.py
```

## Endpoints available:


POST - Register an user (example on body request: {"user": "pedro", "password": "myp4ssw0rd"})
```bash
/register
```

POST - Login to the API example: (example on body request: {"user": "pedro", "password": "myp4ssw0rd"})
```bash
/login
```

POST - You need to pass the JWT token on params (Bearer <token>)
```bash
/logout
```

POST - refresh the session token (Bearer <token>)
```bash
/refresh
```

GET - get user information
```bash
/user/<user_id>
```

DEL - delete specific user
```bash
/user/<user_id>
```

GET - get all stores
```bash
/stores
```

GET - get specific store
```bash
/store/<name>
```

POST - add store
```bash
/store/<name>
```

DEL - delete store
```bash
/store/<name>
```

GET - get all items, if you logged in you will get more information
```bash
/items
```

GET - get specific item
```bash
/item/<name>
```

POST - add new item to store (example on body: {"price": 10.24, "store_id": "1"})
```bash
/item/<name>
```

PUT - update the item in the store (example on body: {"price": 10.24, "store_id": "1"})
```bash
/item/<name>
```

DEL - delete specific item
```bash
/item/<name>
```
