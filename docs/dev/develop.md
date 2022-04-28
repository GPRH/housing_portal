# Development

To checkout the app, in a terminal run:

`git clone git@github.com:bjohare/wb-housing-prototype.git housing-portal`

The development process uses [docker](https://www.docker.com/) for both local development and for deployment on staging and production environments. Make sure both `docker` and `docker-compose` are [installed](https://docs.docker.com/compose/install/). For local development, the `backend` directory is mounted into the **backend** docker container. The dockerfiles for the backend container are in `backend/compose/local` and `backend/compose/production`.

To launch the containers locally for development run:

`docker-compose -f local.yml up --build`

This will build and run the containers, which can take a while when first run. Once all the containers are started you can view the application in your browser at [http://localhost:8000](http://localhost:8000)

Application components are proxied by Nginx in both development and production / staging environments. See [Nginx](nginx.md). See [Docker Volumes](docker.md) for docker volumes used in development and production.

## Env file

The following `.env` file should be saved into the root folder of the checked out project. The following is an example only and should be populated by your own values.

```bash
DEPLOYMENT_ENV=local

# Vue app will only detect VUE_APP envs

VUE_APP_MAPBOX_ACCESS_TOKEN={{ your mapbox client access token }}
VUE_APP_DOMAIN=http://localhost:8000
VUE_APP_MAPILLARY_CLIENT_ID={{ your mapillary client id }}
VUE_APP_MAPILLARY_USER_ID=sarahantos
VUE_APP_CONTACT_FORM_AUTH_TOKEN=local_auth_token
VUE_APP_PORTAL_COUNTRY=Colombia
VUE_APP_PORTAL_COUNTRY_ISO_CODE=CO
VUE_APP_PORTAL_EXTENTS=-82.353516 -5.484768 -65.478516 13.923404
VUE_APP_PORTAL_CENTER=-73.916016 4.280680

# Instance settings

PORTAL_INSTANCE=Colombia
PORTAL_CITIES=Cartagena,Neiva

# Django

DEBUG=True
SECRET_KEY={{ your secret key }}
BACKEND_PORT=8002

DOMAIN=http://localhost:8000
ALLOWED_HOSTS=*

# Exports dir

EXPORTS_DIR=/exports/

# Email settings, defaults to 1025 and mailhog

#EMAIL_PORT=25
#EMAIL_HOST=localhost

# PostgreSQL

POSTGRES_DB=housingportal
POSTGRES_PASS={{ password }}
POSTGRES_USER={{ user }}
POSTGRES_DOCKER_VOLUME_NAME=housing_portal_postgis_data_colombia
POSTGRES_DOCKER_CONTAINER_NAME=housing_portal_db_colombia

# pgbouncer

DATABASES_HOST=postgres
DATABASES_PORT=5432
DATABASES_USER={{ POSTGRES_USER }
DATABASES_PASSWORD={{ POSTGRES_PASS }}
DATABASES_DBNAME=housingportal
PGBOUNCER_POOL_MODE=transaction
PGBOUNCER_LISTEN_PORT=5439
PGBOUNCER_MAX_CLIENT_CONNECTION=100
PGBOUNCER_DEFAULT_POOL_SIZE=20

# superuser

ADMIN_USER_EMAIL=admin@admin.com
ADMIN_USER_PASS=admin

# Sentry

SENTRY_DSN=
SENTRY_PUBLIC_DSN=
VUE_APP_SENTRY_PUBLIC_DSN=

#S3

AWS_S3_REGION_NAME=us-east-1
AWS_S3_ENDPOINT_URL=s3.amazonaws.com
AWS_STORAGE_BUCKET_NAME={{ your bucket }}
AWS_SECRET_ACCESS_KEY={{ secret_key }}
AWS_ACCESS_KEY_ID={{ access_key_id }}

S3_IMAGE_ROOT=GEP/DRONE/
IMAGE_DIR=/images/

# internal drone imagery

DRONE_IMAGE_DIR=/drone/

LOCAL_EPSG=21896
```
