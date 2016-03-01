
# Delpoyment

## Create app
```
heroku create trackem
```

## Test locally
```
heroku local web
```

## Deployment
```
git push heroku master
heroku logs --tail
```


## Database
Local database: `postgres://trackemg:trackem@localhost:5432`

### Initialize migrate
```
python manage.py db init
```

```
# create new migration patch into migrations/versions/
python manage.py db migrate
```

Tweak `migrations/versions/:version_hash.py`. Eg. add Postgres enum type:
```
user_status_enum.create(op.get_bind())
```

# Bullets to tackle
 - database
 	- local setup.
 	- enums.
 - SSL
 	- force ssl
 	- create & get certs
 	- install certs

# Captain's log
2016-03-01 09:22: Smokes from production.
2016-03-01 13:05: unittest proof-of-concept using sqlite.
2016-03-01 13:55: flask-restful GET/POST smokes (with Chrome/Postman)
