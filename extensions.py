from flask_wtf import CSRFProtect
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
