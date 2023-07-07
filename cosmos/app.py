from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

# custom modules
from cosmos.middlewares import (
    CSRFMiddleware,
    LgCdnBase64BodyMiddleware,
    RequestLogger,
    RequestID
)


def init_app(
    use_rate_limitter:bool=False,
    use_csrf:bool=False,
):
    app = FastAPI()

    if use_rate_limitter:
        from cosmos.utils.ratelimitter import limiter

        # add rate limitter
        app.state.limitter = limiter

    # add middlewares
    app.add_middleware(
        ProxyHeadersMiddleware, trusted_hosts="*"
    )  # add proxy headers to prevent logging IP address of the proxy server instead of the client
    app.add_middleware(GZipMiddleware, minimum_size=500)  # add gzip compression

    # add custom middlewares
    app.add_middleware(LgCdnBase64BodyMiddleware)
    app.add_middleware(RequestLogger)
    app.add_middleware(RequestID)

    # check if CSRF middleware is enabled
    if use_csrf:
        app.add_middleware(CSRFMiddleware)

    return app


def add_api_routers(app:FastAPI):
    pass
