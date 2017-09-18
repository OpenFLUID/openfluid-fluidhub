
# Overview

Software infrastructure for OpenFLUID FluidHub services, based on Docker containers managed by docker-compose


# Requirements

* docker
* docker-compose


# Run

## Production
```
FLUIDHUB_DATAPATH=/path/to/data docker-compose up
```

## Development
```
FLUIDHUB_DATAPATH=./_dev/server/data docker-compose -f docker-compose.yml -f docker-compose-dev.yml up
```

### Tests

Required python packages:
* sh
* requests

Run the [nosetests](http://nose.readthedocs.io) tool from the source code root directory:
```
nosetests
```
For a more detailed execution of tests, you can add verbosity and stdout options:
```
nosetests --verbosity=3 -s
```

# References

* http://flask.pocoo.org/docs/0.12/
* https://flask-httpauth.readthedocs.io/en/latest/
* https://code-maven.com/deploying-python-flask-using-uwsgi-on-ubuntu-14-04
* http://stewartjpark.com/2015/01/02/implementing-a-git-http-server-in-python.html
