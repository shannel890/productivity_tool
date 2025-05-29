import os
import sys
from pathlib import Path
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from app.models import db, User, Role
from app.resources.chat import ChatResource

def create_app(config_class="config.Config"):
    try:
        app = Flask(__name__)
        print(f"Loading config from {config_class}")
        app.config.from_object(config_class)
        print("Config loaded successfully")

        db.init_app(app)
        print("Database initialized")
        
        migrate = Migrate(app, db)
        print("Migrations initialized")
        
        api = Api(app)
        print("API initialized")

        from app.auth import auth_bp
        app.register_blueprint(auth_bp)
        print("Auth blueprint registered")

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security(app, user_datastore)
        print("Security initialized")

        api.add_resource(ChatResource, '/api/chat')
        print("Chat resource added")

        @app.route('/')
        def index():
            return render_template('index.html')

        print("Application created successfully")
        return app
        
    except Exception as e:
        print(f"Error creating app: {str(e)}", file=sys.stderr)
        raise
        import traceback
        print(f"Error creating app: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        raise
