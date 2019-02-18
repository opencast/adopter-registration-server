from app.models import *
from flask import request

# Create schemata
statistic_report_schema = StatisticsReportSchema(strict=True)
statistic_reports_schema = StatisticsReportSchema(many=True, strict=True)


# Create statistics report
@app.route('/statistics_report', methods=['POST'])
def add_statistics_report():
    from_date = datetime.datetime.strptime(request.json["from_date"], '%Y-%m-%d')
    to_date = datetime.datetime.strptime(request.json["to_date"], '%Y-%m-%d')
    opencast_version = request.json["opencast_version"]

    new_report = StatisticsReport(from_date, to_date, opencast_version)

    db.session.add(new_report)
    db.session.commit()

    return statistic_report_schema.jsonify(new_report)


# Get all statistics reports
@app.route('/statistics_report',methods=['GET'])
def get_statistics_reports(limit=None, offset=None):
    if request.args.get('__limit'):
        limit = request.args.get('__limit')
    if request.args.get('__offset'):
        offset = request.args.get('__offset')
    all_reports = StatisticsReport.query.limit(limit).offset(offset).all()
    return statistic_reports_schema.jsonify(all_reports)


# Get statistics report by id
@app.route('/statistics_report/<id>',methods=['GET'])
def get_statistics_report(id):
    report = StatisticsReport.query.get(id)
    return statistic_report_schema.jsonify(report)

'''
THIS IS AN EXAMPLE HOW TO CREATE AN 'PUT' OR 'DELETE' ENDPOINT


# Update statistics report by id
@app.route('/statistics_report/<id>', methods=['PUT'])
def update_statistics_report(id):
    report = StatisticsReport.query.get(id)

    from_date = datetime.datetime.strptime(request.json["from_date"], '%Y-%m-%d')
    to_date = datetime.datetime.strptime(request.json["to_date"], '%Y-%m-%d')
    opencast_version = request.json["opencast_version"]

    report.from_date = from_date
    report.to_date = to_date
    report.opencast_version = opencast_version

    db.session.commit()

    return statistic_report_schema.jsonify(report)


# Delete statistics report by id
@app.route('/statistics_report/<id>',methods=['DELETE'])
def delete_statistics_report(id):
    report = StatisticsReport.query.get(id)
    db.session.delete(report)
    db.session.commit()
    return statistic_report_schema.jsonify(report)
'''


@app.route('/')
def home():
    return "<h1>Hello World!<h1>"
