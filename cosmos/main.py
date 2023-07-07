from fastapi import Request
import sys

# configure the directory name heytechnonia as a package
sys.path.append(".")
sys.path.append("..")


# custom modules
from cosmos.app import init_app, add_api_routers
from cosmos.utils.logging import Logger


# init fastapi
app = init_app(use_rate_limitter=True)

# start up event
@app.on_event("startup")
async def startup_event():
    Logger().get_logger()  # init logger before app starts up


# shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.get("/")
async def root(request: Request):
    pass


# add API routes
add_api_routers(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
