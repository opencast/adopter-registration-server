from enum import Enum

from app.models import *
from app.errors import *
from flask import request

# Create schemata
statistic_report_schema = StatisticsReportSchema(strict=True)
statistic_reports_schema = StatisticsReportSchema(many=True, strict=True)
error_event_schema = ErrorEventSchema(strict=True)
error_events_schema = ErrorEventSchema(many=True, strict=True)
adopter_schema = AdopterSchema(strict=True)
adopters_schema = AdopterSchema(many=True, strict=True)


def get_adopter_dict_from_request():
    required_fields = ["adopter_key", "type", "country", "area_code", "city", "street", "street_no",
                       "using_opencast_since", "allows_statistics", "allows_error_reports"]

    optional_fields = ["mail", "phone_contact"]

    payload = dict()

    for field in required_fields:
        if field not in request.json:
            raise InvalidUsage("ERROR: At least one required field is missing: '" + field + "'", status_code=400)
        if field == "type":
            if request.json["type"] == "organisation":
                required_fields += ["organisation_name"]
                optional_fields += ["gender", "first_name", "last_name"]
            elif request.json["type"] == "person":
                required_fields += ["gender", "first_name", "last_name"]
                optional_fields += ["organisation_name"]
            else:
                raise InvalidUsage("Invalid argument for 'type'", status_code=400)

        if field == "gender":
            if request.json[field] not in ["male", "female"]:
                raise InvalidUsage("Invalid argument for 'gender'", status_code=400)
        payload[field] = request.json[field]

    for field in optional_fields:
        if field in request.json:
            if field == "gender":
                if request.json[field] not in ["male", "female"]:
                    raise InvalidUsage("Invalid argument for 'gender'", status_code=400)
            payload[field] = request.json[field]
        else:
            payload[field] = None

    return payload


# Create adopter
@app.route('/api/1.0/adopter', methods=['POST'])
def add_adopter():
    payload = get_adopter_dict_from_request()

    new_adopter = Adopter()
    new_adopter.update(payload)
    db.session.add(new_adopter)
    db.session.commit()

    return adopter_schema.jsonify(new_adopter)

# Get all adopters
@app.route('/api/1.0/adopter',methods=['GET'])
def get_adopters(limit=None, offset=None):
    if request.args.get('__limit'):
        limit = request.args.get('__limit')
    if request.args.get('__offset'):
        offset = request.args.get('__offset')
    all_adopters = Adopter.query.limit(limit).offset(offset).all()
    return adopters_schema.jsonify(all_adopters)

# Get adopter report by adopter_key
@app.route('/api/1.0/adopter/<adopter_key>',methods=['GET'])
def get_adopter(adopter_key):
    a = Adopter.query.get(adopter_key)
    return adopter_schema.jsonify(a)


# Update adopter by adopter_key
@app.route('/api/1.0/adopter/<adopter_key>', methods=['PUT'])
def update_adopter(adopter_key):
    adopter = Adopter.query.get(adopter_key)
    if adopter is None:
        raise InvalidUsage("Adopter with id '" + adopter_key + "' not found")
    payload = get_adopter_dict_from_request()

    for col in ["adopter_key", "created", "last_activity"]:
        if col in payload:
            del payload[col]

    adopter.update(payload)
    db.session.commit()

    return adopter_schema.jsonify(adopter)


# Create statistics report
@app.route('/api/1.0/statistics_report', methods=['POST'])
def add_statistics_report():
    from_date = datetime.datetime.strptime(request.json["from_date"], '%Y-%m-%d')
    to_date = datetime.datetime.strptime(request.json["to_date"], '%Y-%m-%d')
    opencast_version = request.json["opencast_version"]
    adopter_key = request.json["adopter_key"]
    adopter = Adopter.query.get(adopter_key)
    if adopter is None:
        raise InvalidUsage("No adopter found with this key", status_code=400)

    new_report = StatisticsReport()
    new_report.update({"adopter_key": adopter_key, "from_date": from_date, "to_date": to_date, "opencast_version": opencast_version})

    db.session.add(new_report)
    db.session.commit()

    return statistic_report_schema.jsonify(new_report)


# Get all statistics reports
@app.route('/api/1.0/statistics_report',methods=['GET'])
def get_statistics_reports(limit=None, offset=None):
    if request.args.get('__limit'):
        limit = request.args.get('__limit')
    if request.args.get('__offset'):
        offset = request.args.get('__offset')
    all_reports = StatisticsReport.query.order_by(StatisticsReport.to_date.desc()).limit(limit).offset(offset).all()
    return statistic_reports_schema.jsonify(all_reports)

# Get all statistics reports by  adopter
@app.route('/api/1.0/adopter/<adopter_key>/statistics_report',methods=['GET'])
def get_statistics_reports_by_adopter(adopter_key, limit=None, offset=None):
    adopter = Adopter.query.get(adopter_key)
    if adopter is None:
        raise InvalidUsage("Adopter with id '" + adopter_key + "' not found")

    if request.args.get('__limit'):
        limit = request.args.get('__limit')
    if request.args.get('__offset'):
        offset = request.args.get('__offset')
    all_reports = StatisticsReport.query.filter_by(adopter_key=adopter_key)\
        .order_by(StatisticsReport.to_date.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
    return statistic_reports_schema.jsonify(all_reports)


# Get statistics report by id
@app.route('/api/1.0/statistics_report/<id>',methods=['GET'])
def get_statistics_report(id):
    report = StatisticsReport.query.get(id)
    return statistic_report_schema.jsonify(report)


# ERROR EVENT

# Create error event
@app.route('/api/1.0/error_event', methods=['POST'])
def add_error_event():
    timestamp = datetime.datetime.strptime(request.json["timestamp"], '%Y-%m-%dT%H:%M:%S%z')
    print(timestamp)
    error_type = request.json["error_type"]
    data = request.json["data"]
    adopter_key = request.json["adopter_key"]
    opencast_version = request.json["opencast_version"]
    adopter = Adopter.query.get(adopter_key)
    if adopter is None:
        raise InvalidUsage("No adopter found with this key", status_code=400)

    new_error_event = ErrorEvent()
    new_error_event.update({"adopter_key": adopter_key, "opencast_version": opencast_version, "timestamp": timestamp, "error_type": error_type, "data": data})

    db.session.add(new_error_event)
    db.session.commit()

    return error_event_schema.jsonify(new_error_event)


# Get all error events
@app.route('/api/1.0/error_event',methods=['GET'])
def get_error_events(limit=None, offset=None):
    if request.args.get('__limit'):
        limit = request.args.get('__limit')
    if request.args.get('__offset'):
        offset = request.args.get('__offset')
    all_events = ErrorEvent.query.order_by(ErrorEvent.timestamp.desc()).limit(limit).offset(offset).all()
    return error_events_schema.jsonify(all_events)


# Get all error events by  adopter
@app.route('/api/1.0/adopter/<adopter_key>/error_event',methods=['GET'])
def get_error_events_by_adopter(adopter_key, limit=None, offset=None):
    adopter = Adopter.query.get(adopter_key)
    if adopter is None:
        raise InvalidUsage("Adopter with id '" + adopter_key + "' not found")

    if request.args.get('__limit'):
        limit = request.args.get('__limit')
    if request.args.get('__offset'):
        offset = request.args.get('__offset')
    all_events = ErrorEvent.query.filter_by(adopter_key=adopter_key)\
        .order_by(ErrorEvent.timestamp.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
    return error_events_schema.jsonify(all_events)


# Get error event by id
@app.route('/api/1.0/error_event/<id>',methods=['GET'])
def get_error_event(id):
    error_event = ErrorEvent.query.get(id)
    return error_event_schema.jsonify(error_event)

'''
THIS IS AN EXAMPLE HOW TO CREATE A 'DELETE' ENDPOINT

# Delete statistics report by id
@app.route('/api/1.0/statistics_report/<id>',methods=['DELETE'])
def delete_statistics_report(id):
    report = StatisticsReport.query.get(id)
    db.session.delete(report)
    db.session.commit()
    return statistic_report_schema.jsonify(report)
'''


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
