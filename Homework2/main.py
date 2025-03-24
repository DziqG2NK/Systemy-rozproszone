# Small API app for listing people on ISS and current location of ISS
# http://open-notify.org/Open-Notify-API/?ref=public_apis&utm_medium=website
# https://opencagedata.com/api#quickstart
# https://tle.ivanstanojevic.me/#/
# taskkill /F /IM python.exe

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from data import data

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_position(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/response")
async def get_response(request: Request, satellite_name: str=""):

    satellite_data = await data(satellite_name)
    satellite = {
        "name": satellite_name,
        "latitude": satellite_data["cords"]["latitude"],
        "longitude": satellite_data["cords"]["longitude"],
        "continent": satellite_data["region"]["continent"],
        "district": satellite_data["region"]["district"],
        "country": satellite_data["region"]["country"]
    }

    return templates.TemplateResponse("response.html", {
            "request": request,
            "satellite": satellite
        })


# @app.get("/getJSON")
# async def get_json(url: str):
#     r = await get_info_from_api(url, params=None)
#     print(r)
#     return
#     # return get_info_from_api("http://api.open-notify.org/astros.json", params=None)
#
# @app.get("/getsomething")
# async def get_some():
#     r = httpx.get("http://127.0.0.1:8000/")
#     return r.text
# @app.get("/gfd/")
# async def get_position(request: Request):
    # return templates.TemplateResponse("response.html", {"request": request, "satelite": })

