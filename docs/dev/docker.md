# Docker Volumes

[Docker volumes](https://docs.docker.com/storage/volumes/) are a key part of the Housing Portal architecture.

## Docker volumes for development

### Backend

The local development environment requires a number of docker volumes. These are generally bind mounted from the host file system to the container. For the _backend_ the volumes required are (paths are relative to the project root folder):

```txt
- ../images - the street view images for the portal
- ../imports - where the import script looks for geopackages to import
- ../drone - where the aerial imagery for an instance is stored.
```

A docker volume `exports` is also mounted to the backend container to store portal downloads. See `local.yml` for details of how these volumes are configured for the **backend** container.

### Nginx

The following volumes are required for the Nginx development container:

```txt
- ./backend/media/:/media/
- ./backend/staticfiles/:/staticfiles/
- ./nginx/dev.conf:/etc/nginx/nginx.conf:ro
- ../tiles:/data
- ../images:/images:ro
- ./docs/_build/html:/docs:ro
- ./drone:/drone-viewer:ro
- ../drone:/drone:ro
- exports:/exports:ro
```

### Posgis

Dedicated docker volumes are used for PostGIS data storage, a separate one is used for each portal instance. See `local.yml` and `staging.yml` for examples of how to configure these.

## Docker volumes for staging / production

Best practices dictate that docker volumes should live on a cloud storage volume, for example a Digital Ocean or AWS EBS Volume. This EBS volume should be backed up regularly. As per the development environment, the production environment requires that a number of docker volumes be mounted to the system containers as follows (assuming `/mnt/data` is an EBS volume):

### Backend

```txt
- /mnt/data/imports:/imports
- /mnt/data/exports:/exports
- /mnt/data/images:/images
- /mnt/data/drone:/drone
```

In the above `backend` container configuration, directories on the host machine with prefix `/mnt/data/` are mounted to the container. So for example, `/mnt/data/imports` on the host filesystem becomes `/imports` on the container. The volumes `/images`, `/imports`, `/exports` and `/drone` are **_required_** for the backend container to function correctly.

### Postgis

Each portal instance has it's own dedicated PostGIS instance, which in turn, has its own dedicated docker storage volume. The storage volume is mounted to the `/var/lib/postgresql` directory on the container. See `staging.yml` for volume configuration for the staging PostGIS instance.
