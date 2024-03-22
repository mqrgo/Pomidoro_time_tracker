from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from .crud import add_user_in_db
from .schemes import UserData

router = APIRouter(prefix='/auth', tags=['authentication'])
templates = Jinja2Templates('../templates')


@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/signup')
async def signup(request: Request):
    return templates.TemplateResponse('signup.html', {'request': request})


@router.post('/signup_process')
async def signup_process(username=Form(), email=Form(), password=Form()):
    res = add_user_in_db(username=username, email=email, password=password)
    if res is True:
        return {'res': 'success'}
    return
