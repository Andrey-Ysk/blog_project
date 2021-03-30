from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_mail import Mail
import os

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
app.config['CKEDITOR_PKG_TYPE'] = 'basic'


db = SQLAlchemy(app=app, metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.signin'
moment = Moment(app)
ckeditor = CKEditor(app)
mail = Mail(app)

from .main import main as main_bp
app.register_blueprint(main_bp)
