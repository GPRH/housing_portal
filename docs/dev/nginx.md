# Nginx

Nginx is used as a reverse proxy in both local development and in production / staging environments. In development,
nginx is run from a docker container. The configuration file for this nginx instance is at `nginx/dev.conf` in the source. See the docker compose file at `local.yml` for details of this containers configuration.

In staging / production environments nginx is installed on the host machine during application deployment using ansible. The ansible tasks for nginx installation is at `provision/tasks/nginx.yml`. The nginx configuration for staging / production is at `provision/files/nginx_site.conf`. This file is an ansible template which is injected with variables from the `deploy/{country}_vars.yml` file during deployment.
