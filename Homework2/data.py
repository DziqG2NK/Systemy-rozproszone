import httpx
import asyncio
import json
from datetime import datetime

from fastapi import HTTPException
from sgp4.api import Satrec
from math import atan2, sqrt, degrees

from starlette.templating import Jinja2Templates

satellite_location_url = "https://tle.ivanstanojevic.me/api/tle/"
geo_url = "https://api.opencagedata.com/geocode/v1/json"
geo_api_key = "e2357fc9ddfb401bade0d477f1f0ce7e"

templates = Jinja2Templates(directory="templates")

async def get_info_from_api(url: str, params=None):
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.get(url=url, params=params)
        print(response.request)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Couldn't get info from API")

        return response.text

async def get_orbital_params(satellite_id: int):
    url = satellite_location_url + str(satellite_id)
    response = await get_info_from_api(url=url)

    response = json.loads(response)

    orbital_params = {
    "date": response["date"],
    "line_1": response["line1"],
    "line_2": response["line2"]
    }

    return orbital_params

def convert_cords(r):
    r_x, r_y, r_z = r

    longitude = atan2(r_y, r_x)

    r_xy = sqrt(r_x ** 2 + r_y ** 2)
    latitude = atan2(r_z, r_xy)

    longitude_deg = degrees(longitude)
    latitude_deg = degrees(latitude)

    return latitude_deg, longitude_deg

def get_cords(orbital_params: dict):
    satellite = Satrec.twoline2rv(orbital_params["line_1"], orbital_params["line_2"])

    date = datetime.fromisoformat(orbital_params["date"])
    jd = date.toordinal() + 1721424.5 + (date.hour + date.minute / 60 + date.second / 3600) / 24
    fr = (date.hour + date.minute / 60 + date.second / 3600) / 24

    e, r, v = satellite.sgp4(jd, fr)
    try:
        latitude, longitude = convert_cords(r)
    except Exception as e:
        raise HTTPException(status_code=403, detail="Error converting coordinates")

    cords = {
        "latitude": latitude,
        "longitude": longitude
    }

    return cords

async def get_geo_json(latitude: float, longitude: float):
    geo_q = str(round(latitude, 7)) + "," + str(round(longitude, 7))
    print(geo_q)

    geo_params = {
        "key": geo_api_key,
        "q": geo_q,
        "pretty": 1,
        "no_annotations": 1
    }

    response = await get_info_from_api(geo_url, geo_params)
    response = json.loads(response)

    return response

async def get_country(cords: dict):
    latitude = cords["latitude"]
    longitude = cords["longitude"]

    response = await get_geo_json(latitude, longitude)

    components = response["results"][0]["components"]
    region = None

    if "continent" in components:
        region = {
            "continent": components["continent"],
            "country": components["country"],
        }
        if "district" in components:
            region["district"] = components["district"]

    elif not "continent" in components:
        region = {
            "body_of_water": components["body_of_water"]
        }

    if region is None:
        raise HTTPException(status_code=404, detail="Couldn't find region for satellite")

    print(region)
    return region


async def data(satellite_name):
    satellite_id = None

    match satellite_name:
        case "ISS":
            satellite_id = 25544
        case "LANDSAT 9":
            satellite_id = 49260
        case "AISSAT 2":
            satellite_id = 40075
        case "AISSAT 1":
            satellite_id = 40075
        case "NOAA 19":
            satellite_id = 33591
        case "NOAA 18":
            satellite_id = 28654
        case "ZHUHAI-1 02":
            satellite_id = 42759
        case "PROXIMA II":
            satellite_id = 43696
        case "PROXIMA I":
            satellite_id = 43694
        case "SWISSCUBE":
            satellite_id = 35932

    if satellite_id is None:
        raise HTTPException(status_code=404, detail="Satellite not found")

    params = await get_orbital_params(satellite_id)
    cords =  get_cords(params)
    region = await get_country(cords)

    satellite_data = {
        "cords": cords,
        "region": region
    }

    return satellite_data