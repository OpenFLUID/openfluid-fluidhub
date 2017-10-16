
# Overview

Software infrastructure for OpenFLUID FluidHub services, based on Docker containers managed by docker-compose


# Requirements

* docker (>= 17.06)
* docker-compose


# Production mode


## Initialize

The initialization consists in creating the data directory with the minimal required structure.
It also creates a default `admin` user with password `admin`. It is really encouraged to change this password immediately.

From the root of the source tree, use the `prod-init` wrapper script, with the path of the directory to initialize as an argument:
```
./prod-init /path/to/data
```
**YOU ARE REALLY ENCOURAGED TO CHANGE THE DEFAULT SECRET VALUE IN the `common/local.conf` FILE LOCATED IN YOUR DATA DIRECTORY**

## Build

The build will produced the corresponding Docker image. It should be performed once for all before launching the services.  

From the root of the source tree, use the `prod-server` wrapper script (recommended):
```
FLUIDHUB_DATAPATH=/path/to/data ./prod-server build
```


You can also use the docker-compose command directly:
```
FLUIDHUB_DATAPATH=/path/to/data docker-compose -f docker/docker-compose.yml build
```

## Launch services

The run will launch the services.  

From the root of the source tree, use the `prod-server` wrapper script (recommended):
```
FLUIDHUB_DATAPATH=/path/to/data ./prod-server up
```

You can also use the docker-compose command directly:
```
FLUIDHUB_DATAPATH=/path/to/data docker-compose -f docker/docker-compose.yml up
```

The only username available at first launch is the Adminsitrator with username `admin` and password `admin`.  
**YOU ARE REALLY ENCOURAGED TO CHANGE THE `admin` PASSWORD AT FIRST LAUNCH**


## Deploy through frontend

By default, the FluidHub services runs in HTTP on port 3447 of a Docker container.  
You have to configure an http server in HTTPs mode, such as Apache or Nginx, to redirect the incoming HTTPs stream to this HTTP port.



# Development mode


The source tree is organized as below:
```
/fluidhub
  /app        -> main application source code
  /FluidHub   -> FluidHub package containing common modules
/resources    -> various ressources
/tests        -> tests source code and resources
/docker       -> configurations for Docker containers and docker-compose
```

## Initialize

The initialization consists in creating the data directory with the minimal required structure withinin the `_dev` subdirectory.
It also creates a default `admin` user with password `admin`.

From the root of the source tree, use the `dev-init` wrapper script:
```
./dev-init
```


## Launch services

The run will launch the services currently under development.  

From the root of the source tree, use the `dev-server` wrapper script (recommended), the `FLUIDHUB_DATAPATH` environment variable is automatically set:
```
./dev-server up
```

You can also use the docker-compose command directly:
```
FLUIDHUB_DATAPATH=./_dev/server/data docker-compose -f docker/docker-compose.yml -f docker/docker-compose-dev.yml up
```


## Run tests


Run the [nosetests](http://nose.readthedocs.io) tool from the root of the source tree, using the `dev-runtests` wrapper script:
```
./dev-runtests nosetests
```
For a more detailed execution of tests, you can add verbosity and stdout options:
```
./dev-runtests nosetests --verbosity=3 -s
```

# External resources

* http://flask.pocoo.org/docs/0.12/
* https://flask-httpauth.readthedocs.io/en/latest/
* https://code-maven.com/deploying-python-flask-using-uwsgi-on-ubuntu-14-04
* http://stewartjpark.com/2015/01/02/implementing-a-git-http-server-in-python.html
* https://pyjwt.readthedocs.io/en/latest/
* https://www.sqlalchemy.org/
* http://nose.readthedocs.io/en/latest/index.html
