import uuid

from fastapi import APIRouter, Depends, status, HTTPException, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from applications.database.session_dependencies import get_async_session
from applications.users.crud import (
    create_user_in_db,
    get_user_by_email,
    activate_user_account,
)
from applications.users.shemas import RegisterUserFields, BaseUserInfo

from services.rabbit.constants import SupportedQueues
from services.rabbit.rabbitmq_service import rabbitmq_broker

router_users = APIRouter()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    new_user: RegisterUserFields,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
) -> BaseUserInfo:
    user = await get_user_by_email(new_user.email, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Already exists"
        )

    created_user = await create_user_in_db(
        new_user.email, new_user.name, new_user.password, session
    )
    # await rabbitmq_broker.send_message(
    #     message={"name": created_user.name, "email": created_user.email,
    #              'redirect_url': str(request.url_for('verify_user', user_uuid=created_user.uuid_data))
    #              },
    #     queue_name=SupportedQueues.USER_REGISTRATION)
    background_task.add_task(
        rabbitmq_broker.send_message,
        message={
            "name": created_user.name,
            "email": created_user.email,
            "redirect_url": str(
                request.url_for("verify_user", user_uuid=created_user.uuid_data)
            ),
        },
        queue_name=SupportedQueues.USER_REGISTRATION,
    )

    return created_user


@router_users.get("/verify/{user_uuid}")
async def verify_user(
    user_uuid: uuid.UUID, session: AsyncSession = Depends(get_async_session)
):
    await activate_user_account(user_uuid, session)
    return {"Status": "activated"}
