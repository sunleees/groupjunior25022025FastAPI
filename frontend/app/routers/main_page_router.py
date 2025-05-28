from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("index.html", context=context)
    return response


async def login_user(user_email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="http://backend_api:9999/api/auth/login",
            data={"username": user_email, "password": password},
        )
        print(response.json())


@router.get("/login")
@router.post("/login")
async def login(request: Request, user_email: str = Form(""), password: str = Form("")):
    print(request.method, 555555555)
    print(f"{user_email}")
    print(f"{password}")

    await login_user(user_email, password)

    context = {"request": request}
    response = templates.TemplateResponse("login.html", context=context)
    return response
