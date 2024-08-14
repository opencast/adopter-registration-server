from app.models import *
from app.errors import *
from flask import request
from flask import jsonify
from flask_security.decorators import roles_accepted, http_auth_required
import json

# Create schemata
adopter_schema = AdopterSchema()
adopters_schema = AdopterSchema(many=True)
statistic_schema = StatisticSchema()
statistics_schema = StatisticSchema(many=True)
tobira_schema = TobiraSchema()
tobiras_schema = TobiraSchema(many=True)

# Creates a dictionary from the adopter request
def get_dict_from_request(required_fields, optional_fields):
    #We do this rather than use request.json because OC prior to 12.12/13.7/14.0
    # *claimed* to be sending UTF-8, but was actually sending latin-1 (or system default)
    try:
        req_json = json.loads(request.data)
    except UnicodeDecodeError:
        req_json = json.loads(request.data.decode("latin-1").encode("utf-8"))

    payload = dict()
    for field in required_fields:
        if field not in req_json:
            raise InvalidUsage("ERROR: At least one required field is missing: '" + field + "'", status_code=400)
        payload[field] = req_json[field]

    for field in optional_fields:
        if field in req_json:
            payload[field] = req_json[field]
        else:
            payload[field] = None
    return payload


#================================================================================
# Adopter REST endpoints
#================================================================================

# Create adopter
@app.route('/api/1.0/adopter', methods=['POST'])
def add_adopter():
    required_fields = ['adopter_key']
    optional_fields = ['country', 'postal_code', 'city', 'street', 'street_no',
                       'organisation_name', 'email', 'first_name', 'last_name',
                       'department_name', 'contact_me', 'system_type', 'send_errors', 'send_usage']

    payload = get_dict_from_request(required_fields, optional_fields)
    adopter = Adopter.query.get(payload['adopter_key'])
    if adopter is None:
        adopter = Adopter()
        db.session.add(adopter)
    adopter.update(payload)
    db.session.commit()
    response = adopter_schema.dumps(adopter)
    return jsonify({'adopter' : response})

# Delete adopter
@app.route('/api/1.0/adopter', methods=['DELETE'])
def remove_adopter():
    required_fields = ['adopter_key']
    optional_fields = []

    payload = get_dict_from_request(required_fields, optional_fields)
    adopter = Adopter.query.get(payload['adopter_key'])
    db.session.delete(adopter)
    db.session.commit()
    db.session.flush()
    return jsonify({'deleted' : payload['adopter_key']})

# Get all adopters
@app.route('/api/1.0/adopter',methods=['GET'])
def get_adopters(limit=None, offset=None):
    adopters = Adopter.query.all()
    response = adopters_schema.dump(adopters)
    return jsonify({'adopters' : response})



#================================================================================
# Statistic REST endpoints
#================================================================================

# Create statistics report
@app.route('/api/1.0/statistic', methods=['POST'])
def add_statistic():
    required_fields = ['statistic_key']
    optional_fields = ['adopter_key', 'job_count', 'event_count', 'ca_count',
                       'series_count', 'user_count', 'hosts', 'version',
                       'total_minutes', 'tenant_count']
    payload = get_dict_from_request(required_fields, optional_fields)
    statistic = Statistic.query.get(payload['statistic_key'])
    if statistic is None:
        statistic = Statistic()
        db.session.add(statistic)
    statistic.update(payload)
    db.session.commit()
    response = statistic_schema.dumps(statistic)
    return jsonify({'statistic' : response})

# Delete statistics report
@app.route('/api/1.0/statistic', methods=['DELETE'])
def remove_statistic():
    required_fields = ['statistic_key']
    optional_fields = []

    payload = get_dict_from_request(required_fields, optional_fields)
    hosts = db.session.query(Host).filter(Host.statistic_key == payload['statistic_key']).all()
    for host in hosts:
      db.session.delete(host)

    statistic = Statistic.query.get(payload['statistic_key'])
    if statistic:
        db.session.delete(statistic)

    db.session.commit()
    db.session.flush()
    return jsonify({'deleted' : payload['statistic_key']})

# Get all statistic entries
@app.route('/api/1.0/statistic',methods=['GET'])
def get_statistics(limit=None, offset=None):
    stats = Statistic.query.all()
    response = statistics_schema.dump(stats)
    return jsonify({'statistics' : response})


# Create Tobira report
@app.route('/api/1.0/tobira', methods=['POST'])
def add_tobira():
    required_fields = ['statistic_key', 'data']
    optional_fields = []
    payload = get_dict_from_request(required_fields, optional_fields)
    tobira = Tobira.query.get(payload['statistic_key'])
    if tobira is None:
        tobira = Tobira()
        db.session.add(tobira)
    #Copy this into the data being ingested to Tobira, since we need it there too
    payload['data']['statistic_key'] = payload['statistic_key']
    tobira.update(payload['data'])
    db.session.commit()
    response = tobira_schema.dumps(tobira)
    return jsonify({'tobira' : response})

# Delete Tobira report
@app.route('/api/1.0/tobira', methods=['DELETE'])
def remove_tobira():
    required_fields = ['statistic_key']
    optional_fields = []

    payload = get_dict_from_request(required_fields, optional_fields)
    tobira = Tobira.query.get(payload['statistic_key'])
    db.session.delete(tobira)

    db.session.commit()
    db.session.flush()
    return jsonify({'deleted' : payload['statistic_key']})


# Get all Tobira entries
@app.route('/api/1.0/tobira',methods=['GET'])
def get_tobira(limit=None, offset=None):
    stats = Tobira.query.all()
    response = tobira_schema.dump(tobira)
    return jsonify({'tobira' : response})


@app.route('/')
def home():
    return """
    <html>
    <head>
    <meta http-equiv="refresh" content="0; URL=/admin">
    </head>
    <body>
    <a href="/admin">Weiter zur Admin Page</a>
    </body>
    </html>
    """
