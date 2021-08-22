from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import dotenv_values
import click
from flask.cli import FlaskGroup, ScriptInfo, with_appcontext
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,current_user

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    ensure_dirs_exist(app)
    app.config.from_mapping(dotenv_values(os.path.join(app.instance_path,".env")))

    # Initialise the database into the global variable for use across the app
    db.init_app(app)

    # Initialise the JWT manager
    jwt = JWTManager(app)

    #handle bcrypt
    bcrypt.init_app(app)

    #Handle flask logins
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Initialise the blueprints (routes) for the application
    from . import blueprints
    blueprints.init_blueprints(app)

    #Add CLI options
    app.cli.add_command(init_db_command)
    app.cli.add_command(destroy_db_command)
    app.cli.add_command(create_user)

    #Inject user into every request
    @app.before_request
    def before_request():
        g.user = current_user

        
    return app


def ensure_dirs_exist(app):
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Check to make sure the config file exists. If not, alert user to make the .env file
    if not os.path.isfile(os.path.join(app.instance_path,".env")):
        print("----------------------------------------------------------------------------")
        print("No environment detected! Make a copy of instance/.env.example to instance/.env and modify it to the instance needs")
        print("----------------------------------------------------------------------------") 

        raise("No environment detected! Make a copy of instance/.env.example to instance/.env and modify it to the instance needs")

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    app = create_app()
    from . import models
    db.create_all()

    click.echo('Initialized the database.')

@click.command('destroy-db')
@with_appcontext
def destroy_db_command():
    """Clear the existing data and create new tables."""
    app = create_app()
    from . import models
    db.drop_all()

    click.echo('Destroyed the database.')

@click.command('create-user')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_user(email, password):
    """Clear the existing data and create new tables."""
    from .models import User
    me = User(email, password)
    db.session.add(me)
    db.session.commit()
    click.echo('Created user.')

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.filter_by(email = user_id).first()

