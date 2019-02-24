from app import app, db, ma
import pycountry
import datetime
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

class Adopter(db.Model):
    adopter_key = db.Column(db.String(64), unique=True, nullable=False, primary_key=True, autoincrement=False)
    type = db.Column(db.String(12), nullable=False)
    gender = db.Column(db.String(6))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    organisation_name = db.Column(db.String(100))
    country = db.Column(db.String(3), nullable=False)   # alpha_3
    area_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    street = db.Column(db.String(80), nullable=False)
    street_no = db.Column(db.String(10), nullable=False)
    mail = db.Column(db.String(50))
    phone_contact = db.Column(db.String(50))
    using_opencast_since = db.Column(db.SmallInteger, nullable=False)
    allows_statistics = db.Column(db.Boolean, nullable=False)
    allows_error_reports = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self):
        pass

    def update(self, values):
        for k, v in values.items():
            if k == "type" and v not in ["organisation", "person"]:
                raise ValueError("Invalid argument for 'type'")
            if k == "gender" and (v not in ["male", "female"] and v is not None):
                print(v)
                raise ValueError("Invalid argument for 'gender'")
            setattr(self, k, v)

# Statistics Report Schema
class AdopterSchema(ma.Schema):
    class Meta:
        fields = ('adopter_key', 'type', 'gender', 'first_name', 'last_name', 'organisation_name', 'country',
                  'area_code', 'city', 'street', 'street_no', 'mail', 'phone_contact', 'using_opencast_since',
                  'allows_statistics', 'allows_error_reports', 'created', 'last_activity')

class StatisticsReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    adopter_key = db.Column(db.String(64), db.ForeignKey('adopter.adopter_key'),
        nullable=False)
    opencast_version = db.Column(db.String(20))

    def __init__(self):
        pass

    def update(self, values):
        for k, v in values.items():
            setattr(self, k, v)

class ErrorEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    adopter_key = db.Column(db.String(64), db.ForeignKey('adopter.adopter_key'),
        nullable=False)
    error_type = db.Column(db.String(100))
    data = db.Column(db.Text)
    opencast_version = db.Column(db.String(20))

    def __init__(self):
        pass

    def update(self, values):
        for k, v in values.items():
            setattr(self, k, v)

# Statistics Report Schema
class StatisticsReportSchema(ma.Schema):
    class Meta:
        fields = ('id', 'from_date', 'to_date', 'opencast_version', 'adopter_key')

# ErrorEventSchema
class ErrorEventSchema(ma.Schema):
    class Meta:
        fields = ('id', 'timestamp', 'error_type', 'opencast_version', 'data', 'adopter_key')

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))