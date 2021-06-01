import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # sql alchemy Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False,

    # Flask admin
    FLASK_ADMIN_SWATCH = 'cosmo'

    # Flask-Security config
    # TODO before production: Change password salt
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = 'CHANGE_ME'

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO before production: Change default superuser data or:
    # 1. Run app and register as a user
    # 2. login with default admin
    # 3. give created user the role: superuser
    # 4. delete admin
    DEFAULT_SUPER_USER_MAIL = "admin"
    DEFAULT_SUPER_USER_PASSWORD = "admin"

    SECURITY_TRACKABLE = True