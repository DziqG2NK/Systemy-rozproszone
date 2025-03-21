from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DOGS = [{"name": "Milo", "type": "Goldendoodle"}, {"name": "Jax", "type": "German Shepard"}]

@app.get("/")
async def get_name(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "codingwithroby", "dogs": DOGS })