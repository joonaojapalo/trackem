
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

Tweak `migrations/versions/:version_hash.py`. Eg. drop Postgres enum types manually in downgrade():
```
# declare enum type
enums = [sa.Enum('new', 'confirmed', 'deleted', name="status_enum")]

# drop in upgrade()
    for enum in enums:
        enums.drop(op.get_bind())
```

# Channels
Client-side `Backbone.Radio` channels
 - `navigation`: navigation & routing events


# Bullets to tackle
 - apis
 	- map
 	- race
 	- runner
 - front-end
 	- marionette list views
 	- new object editor
 - andoid app
 	- smokes
 	- location collerctor service
 - SSL
 	- force ssl
 	- create & get certs
 	- install certs

# Captain's log
2016-03-01 09:22: Smokes from production.
2016-03-01 13:05: unittest proof-of-concept using sqlite.
2016-03-01 13:55: flask-restful GET/POST smokes (with Chrome/Postman)
2016-03-01 15:54: smokes in production with db & api
2016-03-02 15:30: login & jade layout
2016-03-02 17:42: coffee script smokes.
2016-03-03 11:13: rest api uunittesting smokes
2016-03-15 11:14: android app smokes.
2016-03-31 12:55: 1st android service bound.
