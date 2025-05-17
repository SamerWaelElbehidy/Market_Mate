from flask import Flask
from flasgger import Swagger
from config import Config
from app.routes import register_routes
from app.db import db
import uuid

def create_default_admin():
    admins_collection = db["admins"]
    if admins_collection.count_documents({}) == 0:  
        default_admin = {
            "admin_ID": "ADM" + str(uuid.uuid4())[:8],
            "email": "admin@Test.com",
            "password": "123123"  
        }
        admins_collection.insert_one(default_admin)
        print("Default admin account created: admin@marketmate.com / admin123")

def create_app():
    app = Flask(__name__, 
                template_folder="templates",
                static_folder="../static",  # Points to the static folder at the root level
                static_url_path='/static'   # URL path for static files
    )
    app.secret_key = Config.SECRET_KEY
    Swagger(app)

    register_routes(app)

    create_default_admin()

    return app