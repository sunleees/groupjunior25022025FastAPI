from fastapi import APIRouter, Depends, status
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from applications.auth.password_handler import PasswordEncrypt
from applications.database.session_dependencies import get_async_session
from applications.users.models import User
from applications.users.shemas import RegisterUserFields, BaseFields


async def create_user_in_db(email, name, password, session: AsyncSession):
    hashed_password = await PasswordEncrypt.get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password, name=name)
    session.add(new_user)
    await session.commit()


async def get_user_by_email(email, session: AsyncSession) -> User | None:
    query = select(User).filter(User.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()
