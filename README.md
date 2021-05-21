# Adopter Statistics

This is a Flask server that is build to collect, store and administrate statistics reports and error events from 
opencast instances (adopters). 
In future opencast versions the admin will be asked to
register the instance and allow sending error reports and monthly statistics reports.

## Installation Guide

- Clone Repository:
	```bash
	git clone https://github.com/opencast/adopter-statistics-server.git
	cd adopter-statistics-server
	```
- Create virtual enviroment:
	```bash
	python -m venv venv
	```
- Activate the environment:
	```bash
	. venv/bin/activate
	```
- Install requirements:
	```bash
	pip install -r requirements.txt
	```
- Configure TODOs in `config.py` (if you want to run it in production)
- Run app:
	```bash
	// ignore following line if running in production
	export FLASK_ENV=development

	flask run
	// if you run into ModuleNotFound-Error try using
	venv/bin/flask run
	```
- Open http://127.0.0.1:5000 (redirect to the admin page)

## Opencast Configuration

By default, Opencast will send data to register.opencast.org.
For testing, you can change that by adding the following configuration option to the `custom.properties`:

```properties
org.opencastproject.adopter.statistic.server.url=http://127.0.0.1:5000/api/1.0/
```

## User model / security:
To ensure security there is a role based user model implemented.
Before handling the first request this app will create the database, create the roles "readonly" and "superuser"
and will create the default superuser defined in `config.py` (default: Email: "admin", "Password": "admin"). This default admin should be configured with a strong
password or be deleted after another superuser was created.

To access the admin page you need to create an account. The created user will not have any permissions.
A superuser needs to edit and add a role to your user profile.

**Roles:**
* readonly: Can see Adopter, Error Event and Statistics Report tables
* superuser: readonly + can edit and delete entries and read/edit/delete users

## Api
### Authentication
Use BasicAuth for authentication.

### Adopter
Method | Endpoint | Description | Auth | Query param 
------ | -------- | ----------- | ---- | -----------
`POST` | `/api/1.0/adopter` | Create Adopter | [everybody] | 
`GET` | `/api/1.0/adopter` | Query all Adopters | [readonly/superuser] | `__limit` & `__offset`
`GET` | `/api/1.0/adopter/<adopter_key>` | Query adopter by adopter_key | [everybody] |
`PUT` | `/api/1.0/adopter/<adopter_key>` | Edit adopter | [everybody] |

**Example:**
```json
{
	"adopter_key": "C2B1262C424F905466FBCF2ACA1148CF",
	"organisation_name": "Example University",
	"department_name": "Mathematics and Computer Science",
	"gender": null,
	"first_name": null,
	"last_name": null,
	"mail": null,
	"country": "GER",
	"postal_code": "12345",
	"city": "Exampletown",
	"street": "Main Street",
	"street_no": "1A",
	"address_additional": null,
	"contact_me": false,
	"allows_statistics": true,
	"allows_error_reports": true,
	"allows_tech_data": true
}
```

### Statistics Report
Method | Endpoint | Description | Auth | Query param 
------ | -------- | ----------- | ---- | -----------
`POST` | `/api/1.0/statistics_report` | Create statistics report (adopter_key needed) | [everybody] | 
`GET` | `/api/1.0/statistics_report` | Query all statistic reports | [readonly/superuser] | `__limit` & `__offset`
`GET` | `/api/1.0/statistics_report/<id>` | Query statistic report by id | [readonly/superuser] | 
`GET` | `/api/1.0/adopter/<adopter_key>/statistics_report` | Query statistics reports from adopter | [everybody] | `__limit` & `__offset`

**Example:**
```json
{
	"from_date": "2019-01-01",
	"to_date": "2019-01-31",
	"opencast_version": "6.0.0",
	"adopter_key": "C2B1262C424F905466FBCF2ACA1148CF"
}
```

### Error Event
Method | Endpoint | Description | Auth | Query param 
------ | -------- | ----------- | ---- | -----------
`POST` | `/api/1.0/error_event` | Create error event (adopter_key needed) | [everybody] | 
`GET` | `/api/1.0/error_event` | Query all error events | [readonly/superuser] | `__limit` & `__offset`
`GET` | `/api/1.0/error_event/<id>` | Query error event by id | [readonly/superuser] | 
`GET` | `/api/1.0/adopter/<adopter_key>/error_event` | Query error events from adopter | [everybody] | `__limit` & `__offset`

**Example:**
```json
{
	"timestamp": "2019-02-24T12:34:56+0100",
	"adopter_key": "C2B1262C424F905466FBCF2ACA1148CF",
	"error_type": "Runtime Exception",
	"data": "{'some': 'json_data'}",
	"opencast_version": "6.0.0"
}
```
