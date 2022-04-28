# Architecture

The application consists of two main components, a backend and a frontend. Spatial and user data is stored in a PostGIS database. All application components are run within docker containers, exept for Nginx in production.

## Backend

The backend component is a [django](https://www.djangoproject.com/) application that handles user authentication and authorisation as well as providing import functionality and the mapping api endpoints. The backend consists of a couple of sub-applications stored in the **apps** directory:

- **geodata**: handles downloads, geojson, vector tile and analysis endpoints
- **users**: user authentication and authorisation

The **compose** directory contains _local_ and _production_ docker files. The **scripts** sub-directory
contains backend server startup scripts for either the django development server (local development) or the [gunicorn](https://gunicorn.org/) WSGI server (production deployment).

The **config** directory contains django settings for _test_, _local_, _staging_ and _production_ environments.

The **requirements** directory contains python requirements files. A **base.txt** file for common requirements,
and **local.txt** and **production.txt** requirements files for _local_ and _production_ environments respectively.
The requirments files are used by the backend's dockerfile to configure the django backend container with python dependencies.

The **static** directory contains image and css files for customizing the django admin interface. These are copied into the
**staticfiles** directory by the django _collectstatic_ command when django boots. This happens both in local development and production environments.

The **templates** directory contains admin, contact and registration related templates.

## Frontend

The frontend is a Single Page [Vue.js](https://vuejs.org) application. The application is built using [Vue CLI 3](https://cli.vuejs.org/). The frontend component has a **src** directory which contains all the Vue javascript code as follows:

- **components**: UI application components (more details below).
- **containers**: main page containers to hold other application components, eg Navbar etc...
- **routes**: frontend url configurations. Controls which components are mapped to which urls.
- **store**: [Vuex](https://vuex.vuejs.org/) application state components.
- **views**: page views. The main map view is rendered by a page at _views/maps/MapViewer.vue_

The **public** directory contains the main _index.html_ file and image directories.

Other important files include:

- **main.js**: application entry point contaning globally available Vue imports.

### Frontend Components

The **src/components** directory contains the frontend application components as follows:

- **analysis**: contains Analysis results panel (passports). Results are calculated in the store using the `analysis` module.
- **charts**: chart components (not currently in use)
- **downloads**: handles downloads
- **draw**: the drawing tool for defining custom analysis areas
- **filters**: map filtering components
- **info**: Passport info panels
- **landing**: Application landing page
- **map**: map rendering and layer switching components
- **mapillary**: the mapillary viewer
- **mixins**: reusable code

## Nginx

[Nginx](https://www.nginx.com/) is used as a reverse proxy in both local development and production deployment. The **nginx** folder cotains a _dev.conf_ nginx config which is used in local development by an nginx instance running inside a docker container. This containers port **80** is mapped to the host machine on port **8000** so that the application can be accessed at **http://localhost:8000**. See the docker-compose file _local.yml_ for details of the nginx container configuration. In production, nginx is installed and configured on the production host using ansible, see [Nginx](nginx.md).

## PostGIS

Postgis is run from a docker container with a dedicated volume for data storage.

## PgBouncer

Because we're generating and serving Mapbox Vector Tiles (MVT) directly from Postgis, [PgBouncer](https://www.pgbouncer.org/) is used to pool connections to PostGIS to avoid connection errors.

## Redis

Selected backend endpoints are cached using Redis, in particular, requests to MVT and passport analytics endpoints.

## Docker compose

See `local.yml`, `staging.yml` or `production.yml` for details of how these components are composed for each of these deployment environments.
