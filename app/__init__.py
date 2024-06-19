from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Redis configuration
app.config['REDIS_URL'] = os.getenv('REDIS_URL')
redis_client = FlaskRedis(app)

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models