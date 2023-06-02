#!/bin/bash

CONTENT_TYPE="Content-Type: application/json; utf-8"
ACCEPT="Accept: application/json"

for i in 2
do
  TMP_ADOPTER="$(mktemp)"
  adopter_uuid=`uuidgen`

  echo '{"adopter_key": "'$adopter_uuid'", "organisation_name": "org", "department_name": "dept", "first_name": "ßÖäASDF", "last_name": "last", "country": "country", "city": "city", "postal_code": "postalcode", "street": "street", "street_no": "4", "email": "test@example.org", "send_errors": false, "send_usage": false, "contact_me": true}' > $TMP_ADOPTER
  curl --header "$CONTENT_TYPE" --header "$ACCEPT" --data "@$TMP_ADOPTER" http://localhost:5000/api/1.0/adopter
  rm -f $TMP_ADOPTER

  for j in 2
  do
    TMP_STAT="$(mktemp)"
    stat_uuid=`uuidgen`
    echo '{"statistic_key": "'$stat_uuid'", "job_count": 0, "event_count": 0, "series_count": 0, "user_count": 1, "ca_count": 47, "total_minutes": 1000000, "tenant_count": 4, "hosts": [{"cores": 4, "max_load": 4.0, "memory": 1073741824, "hostname": "asdf", "services": "service1,\nservice2,\nservice3,\nservice4ä"}, {"cores": 2, "maxLoad": 20.0, "memory": 4, "hostname": "qwertyä", "disk_space": -1}], "version": "ä9.0.0.SNAPSHOT", "adopter_key": "'$adopter_uuid'"}' > $TMP_STAT
    curl --header $CONTENT_TYPE --header $ACCEPT --data "@$TMP_STAT" http://localhost:5000/api/1.0/statistic
    rm -f $TMP_STAT
    curl --header "Content-Type: application/json; utf-8" -X DELETE --data '{"statistic_key": "'$stat_uuid'"}' http://localhost:5000/api/1.0/statistic
  done

  curl --header "Content-Type: application/json; utf8" -X DELETE --data '{"adopter_key": "'$adopter_uuid'"}' http://localhost:5000/api/1.0/adopter
done

echo "There should be no records in the database now.  Modify the code above (removing the DELETEs) to see example data."
