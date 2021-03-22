from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command, Shell
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_moment import Moment
import os, config


#sqlite migration fix
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')


db = SQLAlchemy(app=app, metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'signin'
moment = Moment(app)

from . import views
