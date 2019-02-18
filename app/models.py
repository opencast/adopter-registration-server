from app import app, db, ma
import pycountry
import enum
import datetime

class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class TypeEnum(enum.Enum):
    ORGANIZATION = "organization"
    PERSON = "person"

class Adopter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adopter_key = db.Column(db.String(64), unique=True)
    type = db.Column(db.Enum(TypeEnum))
    gender = db.Column(db.Enum(GenderEnum))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    organisation_name = db.Column(db.String(100))
    country = db.Column(db.String(3))   # alpha_3
    area_code = db.Column(db.String(10))
    city = db.Column(db.String(80))
    street = db.Column(db.String(80))
    street_no = db.Column(db.String(10))
    mail = db.Column(db.String(50))
    phone_contact = db.Column(db.String(50))
    using_opencast_since = db.Column(db.SmallInteger)
    allows_statistics = db.Column(db.Boolean)
    allows_error_reports = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, adopter_key, type, gender, first_name, last_name, organisation_name, country, area_code, city,
                 street, street_no, mail, phone_contact, using_opencast_since, allows_statistics, allows_error_reports):
        self.adopter_key = adopter_key
        self.type = type
        self.gender = gender
        self.first_name = first_name
        self.last_name = last_name
        self.organisation_name = organisation_name
        self.country = country
        self.area_code = area_code
        self.city = city
        self.street = street
        self.street_no = street_no
        self.mail = mail
        self.phone_contact = phone_contact
        self.using_opencast_since = using_opencast_since
        self.allows_statistics = allows_statistics
        self.allows_error_reports = allows_error_reports

# Statistics Report Schema
class Adopter(ma.Schema):
    class Meta:
        fields = ('id', 'from_date', 'to_date', 'opencast_version')

class StatisticsReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    # adopter_key =
    opencast_version = db.Column(db.String(20))

    def __init__(self, from_date, to_date, opencast_version):
        self.from_date = from_date
        self.to_date = to_date
        self.opencast_version = opencast_version

# Statistics Report Schema
class StatisticsReportSchema(ma.Schema):
    class Meta:
        fields = ('id', 'from_date', 'to_date', 'opencast_version')

