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


```bash
POST /register: register an user (example on body request: {"user": "pedro", "password": "myp4ssw0rd"})
POST /login: login to the API example: (example on body request: {"user": "pedro", "password": "myp4ssw0rd"})
POST /logout: you need to pass the JWT token on params (Bearer <token>)
POST /refresh: refresh the session token (Bearer <token>)
GET /user/<user_id>: get user information
DEL /user/<user_id>: delete specific user

GET /stores: get all stores
GET /store/<name>: get specific store
POST /store/<name>: add store
DEL /store/<name>: delete store

GET /items: get all items, if you logged in you will get more information
GET /item/<name>: get specific item
POST /item/<name>: add new item to store (example on body: {"price": 10.24, "store_id": "1"})
PUT /item/<name>: update the item in the store (example on body: {"price": 10.24, "store_id": "1"})
DEL /item/<name>: delete specific item
```
