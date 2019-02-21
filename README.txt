1. CREATE DATABASE:
(python console)
from app import db
db.create_all()

2. CREATE INITIAL USER
(python console)
from app import user_datastore
from app import db
user_datastore.create_user(email="your@mail.com", password="yourPassword")