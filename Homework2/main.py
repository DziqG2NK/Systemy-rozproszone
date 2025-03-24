# Small API app for listing people on ISS and current location of ISS
# http://open-notify.org/Open-Notify-API/?ref=public_apis&utm_medium=website
# https://opencagedata.com/api#quickstart
# https://tle.ivanstanojevic.me/#/
# taskkill /F /IM python.exe

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_position(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/response")
async def get_response(request: Request, satellite_name: str=""):



    satellite = {
        "name": satellite_name,
        "country": "gfd",
        "latitude": "saaa",
        "longitude": "aaaa"
    }

    return templates.TemplateResponse("response.html", {
            "request": request,
            "satellite": satellite
        })

# @app.get("/response")
# async def get_response(request: Request):
#     return templates.TemplateResponse("response.html", {
#         "request": request,
#         "satellite": {
#             "name": "bhgfdkjk",
#             "country": "gfd",
#             "latitude": "saaa",
#             "longitude": "aaaa"
#
#         }
#
#     })



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

