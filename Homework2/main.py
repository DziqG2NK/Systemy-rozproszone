# Small API app for listing people on ISS and current location of ISS
# http://open-notify.org/Open-Notify-API/?ref=public_apis&utm_medium=website
# https://opencagedata.com/api#quickstart
# https://tle.ivanstanojevic.me/#/

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

geo_api_key = "e2357fc9ddfb401bade0d477f1f0ce7e"

geo_api_url = "https://api.opencagedata.com/geocode/v1/"
satelite_location_url = "https://tle.ivanstanojevic.me/#/tle/"
iss_location_api_url = "http://api.open-notify.org/iss-now.json"
astronauts_list_url = "http://api.open-notify.org/astros.json"

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_position(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/gfd/")
async def get_position(request: Request):
    return templates.TemplateResponse("response.html", {"request": request})