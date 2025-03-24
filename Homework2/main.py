# Small API app for listing people on ISS and current location of ISS
# http://open-notify.org/Open-Notify-API/?ref=public_apis&utm_medium=website
# https://opencagedata.com/api#quickstart
# https://tle.ivanstanojevic.me/#/
# taskkill /F /IM python.exe

from fastapi import FastAPI, Request, HTTPException
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
    }

    return templates.TemplateResponse("response.html", {
            "request": request,
            "satellite": satellite,
            "region": satellite_data["region"]
        })

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "error_code": exception.status_code}, status_code=exception.status_code)