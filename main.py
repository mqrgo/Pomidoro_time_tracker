from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.auth.router import router as auth_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('START')
    yield
    print('END')




app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory='templates')
app.mount(path='/static', app=StaticFiles(directory='static'), name='static')
app.include_router(auth_router)



@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})



