from fastapi import FastAPI
from applications.settings import settings
from applications.users.router import router_users


def get_application() -> FastAPI:
    app = FastAPI(root_path="/api", root_path_in_servers=True, debug=settings.DEBUG)
    app.include_router(router_users, prefix="/users", tags=["Users"])

    return app
