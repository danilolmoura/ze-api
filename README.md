# ze-api

Geolocation based API written with Python, Flask and Postgres and Postgis

With ze-api you can save partners that deliver products and its area coverage. After that, you can find the closest partner of a point.

# Table of contents
   * [Setup local environment](#setup-local-environment)
   * [References](#references)

# Setup local environment
Make sure you have docker installed and run the following commands

clone the project

    git clone git@github.com:danilolmoura/ze-api.git

create and run the image locally

    cd ze-api
    docker-compose build
    docker-compose up -d

the running application can be found at

    http://127.0.0.1:5000/

application logs can be found at

	docker ps
	docker logs <container_id>

# References

* [Docker](https://www.docker.com/get-started)
* [Flask](http://flask.palletsprojects.com/en/1.1.x/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/)
i
