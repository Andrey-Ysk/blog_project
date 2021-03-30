from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_mail import Mail


#sqlite migration fix
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}



db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(render_as_batch=True)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.signin'
moment = Moment()
ckeditor = CKEditor()
mail = Mail()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    return app