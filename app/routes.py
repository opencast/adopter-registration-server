from app.models import *
from app.errors import *
from flask import request
from flask import jsonify
from flask_security.decorators import roles_accepted, http_auth_required

# Create schemata
adopter_schema = AdopterSchema(strict=True)
adopters_schema = AdopterSchema(many=True, strict=True)
statistic_schema = StatisticSchema(strict=True)
statistics_schema = StatisticSchema(many=True, strict=True)


# Creates a dictionary from the adopter request
def get_dict_from_request(required_fields, optional_fields):
    payload = dict()
    for field in required_fields:
        if field not in request.json:
            raise InvalidUsage("ERROR: At least one required field is missing: '" + field + "'", status_code=400)
        payload[field] = request.json[field]

    for field in optional_fields:
        if field in request.json:
            payload[field] = request.json[field]
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
                       'department_name']

    payload = get_dict_from_request(required_fields, optional_fields)
    adopter = Adopter.query.get(payload['adopter_key'])
    if adopter is None:
        adopter = Adopter()
        db.session.add(adopter)
    adopter.update(payload)
    db.session.commit()
    response = adopter_schema.dumps(adopter).data
    return jsonify({'adopter' : response})


# Get all adopters
@app.route('/api/1.0/adopter',methods=['GET'])
def get_adopters(limit=None, offset=None):
    adopters = Adopter.query.all()
    response = adopters_schema.dump(adopters).data
    return jsonify({'adopters' : response})



#================================================================================
# Statistic REST endpoints
#================================================================================

# Create statistics report
@app.route('/api/1.0/statistic', methods=['POST'])
def add_statistic():
    required_fields = ['statistic_key']
    optional_fields = ['job_count', 'event_count',
                   'series_count', 'user_count', 'hosts']
    payload = get_dict_from_request(required_fields, optional_fields)
    statistic = Statistic.query.get(payload['statistic_key'])
    if statistic is None:
        statistic = Statistic()
        db.session.add(statistic)
    statistic.update(payload)
    db.session.commit()
    response = statistic_schema.dumps(statistic).data
    return jsonify({'statistic' : response})


# Get all statistic entries
@app.route('/api/1.0/statistic',methods=['GET'])
def get_statistics(limit=None, offset=None):
    stats = Statistic.query.all()
    response = statistics_schema.dump(stats).data
    return jsonify({'statistics' : response})


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
