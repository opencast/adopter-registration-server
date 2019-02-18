from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Init
app = Flask(__name__, instance_relative_config=True)

# Load config
app.config.from_object(Config)

# Init db
db = SQLAlchemy(app)

# Init migrate
migrate = Migrate(app, db)

# init
ma = Marshmallow(app)

from app import models
from app import routes
