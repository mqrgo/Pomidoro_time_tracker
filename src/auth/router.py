from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from src.auth.crud import add_user_in_db, check_user_exist
from src.auth.schemes import UserData

router = APIRouter(prefix='/auth', tags=['authentication'])
templates = Jinja2Templates('templates')


@router.post('/signup_process')
async def signup_process(request: Request, username=Form(), email=Form(), password=Form()):
    res = add_user_in_db(username=username, email=email, password=password)
    if res is True:
        next_page = '/auth/login?signup_data=success'
    else:
        next_page = f'/auth/signup?signup_data={res["res"]}'
    return RedirectResponse(
        url=next_page,
        status_code=status.HTTP_301_MOVED_PERMANENTLY
    )


@router.post('/login_process')
async def login_process(user_exist=Depends(check_user_exist)):
    if (res := user_exist) is True:
        return 'success'
    else:
        return RedirectResponse(
            url=f'/auth/login?login_data={res["err"]}',
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get('/signup')
async def signup(request: Request, signup_data: str = None):
    return templates.TemplateResponse(
        'signup.html',
        {'request': request, 'signup_data': signup_data}
    )


@router.get('/login')
async def login(request: Request, signup_data: str = None, login_data: str = None):
    return templates.TemplateResponse(
        'login.html',
        {'request': request, 'signup_data': signup_data, 'login_data': login_data}
    )
