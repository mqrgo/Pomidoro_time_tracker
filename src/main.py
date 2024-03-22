from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from auth.router import router as auth_router

app = FastAPI()
templates = Jinja2Templates(directory='../templates')
app.mount(path='/static', app=StaticFiles(directory='../static'), name='static')
app.include_router(auth_router)

# print(templates.env.list_templates())


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})



