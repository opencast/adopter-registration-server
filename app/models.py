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
    test_system             = db.Column(db.Boolean())
    send_usage              = db.Column(db.Boolean())
    send_errors             = db.Column(db.Boolean())
    contact_me              = db.Column(db.Boolean())
    created                 = db.Column(db.DateTime, default=datetime.datetime.now)
    updated                 = db.Column(db.DateTime, default=datetime.datetime.now)
    statistics              = db.relationship('Statistic', backref='host', lazy='joined')

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
    test_system = fields.Boolean()
    send_usage = fields.Boolean()
    send_errors = fields.Boolean()
    contact_me = fields.Boolean()
    created = fields.String()
    updated = fields.String()


# ================================================================================
#  Statistic Model
# ================================================================================

# Statistic->Host database model
class Host(db.Model):
    id                      = db.Column(db.Integer, primary_key=True)
    statistic_key           = db.Column(db.String(64), db.ForeignKey('statistic.statistic_key'))
    hostname                = db.Column(db.String(64))
    cores                   = db.Column(db.Integer())
    max_load                = db.Column(db.Float())
    memory                  = db.Column(db.Integer())
    disk_space              = db.Column(db.Integer())
    services                = db.Column(db.String(1024))


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
    job_count               = db.Column(db.BigInteger())
    event_count             = db.Column(db.BigInteger())
    series_count            = db.Column(db.BigInteger())
    user_count              = db.Column(db.BigInteger())
    ca_count                = db.Column(db.Integer())
    total_minutes           = db.Column(db.BigInteger())
    hosts                   = db.relationship('Host', backref='statistic', lazy='joined')
    tenant_count            = db.Column(db.BigInteger())
    adopter_key             = db.Column(db.String(64), db.ForeignKey('adopter.adopter_key'))
    created                 = db.Column(db.DateTime, default=datetime.datetime.now)
    updated                 = db.Column(db.DateTime, default=datetime.datetime.now)
    version                 = db.Column(db.String(50))

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


class Tobira(db.Model):
    statistic_key           = db.Column(db.String(64), unique=True, nullable=False, primary_key=True, autoincrement=False)
    num_realms              = db.Column(db.BigInteger())
    num_blocks              = db.Column(db.BigInteger())

    identifier              = db.Column(db.String(50))
    git_commit_hash         = db.Column(db.String(32))
    build_time_utc          = db.Column(db.String(50))
    git_was_dirty           = db.Column(db.Boolean())

    download_button_shown   = db.Column(db.Boolean())
    auth_mode               = db.Column(db.String(32))
    login_link_overridden   = db.Column(db.Boolean())
    logout_link_overridden  = db.Column(db.Boolean())
    uses_pre_auth           = db.Column(db.Boolean())
    has_narrow_logo         = db.Column(db.Boolean())

    def __init__(self):
        pass

    def update(self, values):
        for k, v in values.items():
            if k == 'id':
                continue
            if k == 'config':
                self.download_button_shown = v['download_button_shown']
                self.auth_mode = v['auth_mode']
                self.login_link_overridden = v['login_link_overridden']
                self.logout_link_overridden = v['logout_link_overridden']
                self.uses_pre_auth = v['uses_pre_auth']
                self.has_narrow_logo = v['has_narrow_logo']
            if k == 'version':
                self.identifier = v['identifier']
                self.build_time_utc = v['build_time_utc']
                self.git_commit_hash = v['git_commit_hash']
                self.git_was_dirty = v['git_was_dirty']
            setattr(self, k, v)

#================================================================================
# Marshmallow schemas for JSON serialization
#================================================================================

# Statistic->Host schema
class StatisticHostSchema(ma.Schema):
    id = fields.String()
    statistic_key = fields.String()
    cores = fields.Integer()
    max_load = fields.Float()
    memory = fields.Integer()
    disk_space = fields.Integer()
    hostname = fields.String()
    services = fields.String()


# Statistic schema
class StatisticSchema(ma.Schema):
    id = fields.String()
    job_count = fields.Integer()
    event_count = fields.Integer()
    series_count = fields.Integer()
    user_count = fields.Integer()
    ca_count = fields.Integer()
    total_minutes = fields.Integer()
    hosts = fields.Nested(StatisticHostSchema, many=True)
    tenant_count = fields.Integer()
    created = fields.DateTime()
    updated = fields.DateTime()
    version = fields.String()

class TobiraVersionSchema(ma.Schema):
    identifier = fields.String()
    build_time_utc = fields.String()
    git_commit_hash = fields.String()
    git_was_dirty = fields.String()

class TobiraConfigSchema(ma.Schema):
    download_button_shown = fields.Boolean()
    auth_mode = fields.String()
    login_link_overridden = fields.Boolean()
    logout_link_overridden = fields.Boolean()
    uses_pre_auth = fields.Boolean()
    has_narrow_logo = fields.Boolean()

class TobiraSchema(ma.Schema):
    id = fields.String()
    statistic_key = fields.String()
    num_realms = fields.Integer()
    num_blocks = fields.Integer()
    version = fields.Nested(TobiraVersionSchema)
    config = fields.Nested(TobiraConfigSchema)


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
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
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
