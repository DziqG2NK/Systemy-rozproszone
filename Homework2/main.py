# Small API app for listing people on ISS and current location of ISS
# http://open-notify.org/Open-Notify-API/?ref=public_apis&utm_medium=website
# https://opencagedata.com/api#quickstart
# https://tle.ivanstanojevic.me/#/
# taskkill /F /IM python.exe

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import httpx

geo_api_key = "e2357fc9ddfb401bade0d477f1f0ce7e"

geo_api_url = "https://api.opencagedata.com/geocode/v1/"
satelite_location_url = "https://tle.ivanstanojevic.me/#/tle/43786"
iss_location_api_url = "http://api.open-notify.org/iss-now.json"
astronauts_list_url = "http://api.open-notify.org/astros.json"

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_position(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getJSON")
async def get_json(url: str):
    r = await get_info_from_api(url, params=None)
    print(r)
    return
    # return get_info_from_api("http://api.open-notify.org/astros.json", params=None)

@app.get("/getsomething")
async def get_some():
    r = httpx.get("http://127.0.0.1:8000/")
    return r.text
# @app.get("/gfd/")
# async def get_position(request: Request):
    # return templates.TemplateResponse("response.html", {"request": request, "satelite": })