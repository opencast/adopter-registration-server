from app import app, db, ma
from marshmallow import fields
import datetime
import pycountry
import datetime
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required


# ================================================================================
#  Adopter Model
# ================================================================================

class Adopter(db.Model):
    adopter_key             = db.Column(db.String(64), unique=True, nullable=False, primary_key=True, autoincrement=False)
    first_name              = db.Column(db.String(50))
    last_name               = db.Column(db.String(50))
    organisation_name       = db.Column(db.String(100))
    department_name         = db.Column(db.String(100))
    country                 = db.Column(db.String(3))
    postal_code             = db.Column(db.String(10))
    city                    = db.Column(db.String(80))
    street                  = db.Column(db.String(80))
    street_no               = db.Column(db.String(10))
    email                   = db.Column(db.String(50))
    created                 = db.Column(db.DateTime, default=datetime.datetime.now)
    updated                 = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self):
        pass

    def update(self, values):
        for k, v in values.items():
            if k in ["created", "updated"]:
                continue
            setattr(self, k, v)
        self.updated = datetime.datetime.now()


# Adopter general data schema
class AdopterSchema(ma.Schema):
    adopter_key = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    organisation_name = fields.String()
    department_name = fields.String()
    country = fields.String()
    postal_code = fields.String()
    city = fields.String()
    street = fields.String()
    street_no = fields.String()
    email = fields.String()
    created = fields.String()
    updated = fields.String()


# ================================================================================
#  Statistic Model
# ================================================================================

# Statistic->Host database model
class Host(db.Model):
    id                      = db.Column(db.Integer, primary_key=True)
    statistic_key           = db.Column(db.String, db.ForeignKey('statistic.statistic_key'))
    cores                   = db.Column(db.String(50))
    max_load                = db.Column(db.String(50))
    memory                  = db.Column(db.String(50))

    def __init__(self):
        pass

    def update(self, values):
        for k, v in values.items():
            if k == 'id':
                continue
            setattr(self, k, v)


# Statistic database model
class Statistic(db.Model):
    statistic_key           = db.Column(db.String(64), unique=True, nullable=False, primary_key=True, autoincrement=False)
    job_count               = db.Column(db.String(50))
    event_count             = db.Column(db.String(50))
    series_count            = db.Column(db.String(100))
    user_count              = db.Column(db.String(100))
    hosts                   = db.relationship('Host', backref='statistic', lazy='joined')
    created                 = db.Column(db.DateTime, default=datetime.datetime.now)
    updated                 = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self):
        pass

    def update(self, values):
        for stat_k, stat_v in values.items():
            if stat_k == 'hosts':
                if self.hosts is not None:
                    for db_host in self.hosts:
                        db.session.delete(db_host)
                new_host_list = []
                for host in stat_v:
                    new_host = Host()
                    new_host.update(host)
                    new_host_list.append(new_host)
                stat_v = new_host_list
            setattr(self, stat_k, stat_v)
        self.updated = datetime.datetime.now()


#================================================================================
# Marshmallow schemas for JSON serialization
#================================================================================

# Statistic->Host schema
class StatisticHostSchema(ma.Schema):
    id = fields.String()
    statistic_key = fields.String()
    cores = fields.String()
    max_load = fields.String()
    memory = fields.String()


# Statistic schema
class StatisticSchema(ma.Schema):
    statistic_key = fields.String()
    job_count = fields.String()
    event_count = fields.String()
    series_count = fields.String()
    user_count = fields.String()
    hosts = fields.Nested(StatisticHostSchema, many=True)
    created = fields.DateTime()
    updated = fields.DateTime()


# ================================================================================
#  User Stuff
# ================================================================================

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