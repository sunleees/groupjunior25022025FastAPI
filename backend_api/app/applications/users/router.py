from fastapi import APIRouter, status
from app.applications.users.shemas import RegisterUserFields, BaseFields
from app.settings import settings

router_users = APIRouter()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: RegisterUserFields) -> BaseFields:
    print(settings.POSTGRES_DB, 6666666666666666666666)
    return new_user
