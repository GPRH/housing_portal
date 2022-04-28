# Caching strategies

## Backend

[Redis](https://redis.io/) is used for backend server-side caching in the Housing Portal. There are a couple of areas of **backend** functionality that require caching:

- **Vector Tiles**: mapping tiles are served directly from an api endpoint and are cached in redis to prevent too many requests to the database.
- **Analysis**: caclulating analysis statistics is an expensive operation, particularly for large Areas of Interest. Request to all analysis endpoints are cached in redis.

Caching values for the backend are set in `apps/geodata/urls.py`. In general, once data is imported into the portal it is unlikely to change too frequently. It make sense then to use longer caching values. When data is imported the cache is flushed so that the data and the cache remain in sync.

## Frontend

Since the frontend is a Single Page App, the best practice is not to cache the `index.html` page. The nginx configuration prevents caching of `index.html` by setting `no-store` as the `Cache-Control` http header value. The VueJS javascript files are [cache busted](https://www.keycdn.com/support/what-is-cache-busting#:~:text=Cache%20busting%20solves%20the%20browser,server%20for%20the%20new%20file.) by the webpack build process by default.
