from flask import Flask, url_for
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from config import Config

# Init
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'super secret key'

# Load config
app.config.from_object(Config)

# Init db
db = SQLAlchemy(app)

# Init migrate
migrate = Migrate(app, db)

# init marshmallow
ma = Marshmallow(app)


# init admin
admin = Admin(
    app,
    name='Adopter Statistics Admin',
    base_template='my_master.html',
    template_mode='bootstrap3')


from app import errors
from app import models
from app import routes
from app import views


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

#create roles if not exists
def create_roles_if_not_exists():
    super_user_role_exists = False
    reader_role_exists = False
    super_user_exists = False
    roles = models.Role.query.all()
    super_user_role = None
    for role in roles:
        if role.name == "superuser":
            super_user_role_exists = True
            super_user_role = role
        if role.name == "readonly":
            reader_role_exists = True

    if not super_user_role_exists:
        super_user_role = models.Role(name="superuser")
        db.session.add(super_user_role)
        db.session.commit()
        print("Added superuser role")

    if not reader_role_exists:
        reader_role = models.Role(name="readonly")
        db.session.add(reader_role)
        db.session.commit()
        print("Added readonly role")

    # Check if super user exists
    users = models.User.query.all()
    for user in users:
        if super_user_role in user.roles:
            super_user_exists = True
            break

    # Create super user if not
    if not super_user_exists:
        if "DEFAULT_SUPER_USER_MAIL" not in app.config:
            raise RuntimeError("ERROR: Can't create default superuser. "
                               "DEFAULT_SUPER_USER_MAIL is not defined in config")
        if "DEFAULT_SUPER_USER_PASSWORD" not in app.config:
            raise RuntimeError("ERROR: Can't create default superuser. "
                               "DEFAULT_SUPER_USER_PASSWORD is not defined in config")

        super_user = user_datastore.create_user(email=app.config["DEFAULT_SUPER_USER_MAIL"],
                                 password=app.config["DEFAULT_SUPER_USER_PASSWORD"],
                                 roles=[super_user_role])
        db.session.commit()
        print("Added default superuser!")


app.before_first_request(create_roles_if_not_exists)

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
)