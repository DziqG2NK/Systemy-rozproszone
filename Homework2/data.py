import httpx
import asyncio
import json
from datetime import datetime, timedelta
from sgp4.api import Satrec
from sgp4.api import jday
from math import atan2, sqrt, degrees

satelite_location_url = "https://tle.ivanstanojevic.me/api/tle/"

async def get_info_from_api(url: str, params=None):
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.get(url=url, params=params)
        print(response.request)

        if response.status_code != 200:
            return {"error": "Response from iss error"}

        return response.text

# async def turn_response_to_json(response):

async def get_orbital_params(satellite_id: int):
    url = satelite_location_url + str(satellite_id)
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

    date = datetime.fromisoformat(orbital_params["date"]) + timedelta(hours=-0.75)
    jd = date.toordinal() + 1721424.5 + (date.hour + date.minute / 60 + date.second / 3600) / 24
    fr = (date.hour + date.minute / 60 + date.second / 3600) / 24

    e, r, v = satellite.sgp4(jd, fr)

    latitude, longitude = convert_cords(r)

    print(latitude, longitude)
    return latitude, longitude

# async def get_satellite_location(json_response: dict):



async def main():
    # geo_api_key = "e2357fc9ddfb401bade0d477f1f0ce7e"
    # geo_q = "52.5432379+13.41421330"
    # geo_q = "52.5432379%2C+13.4142133"
    #
    # geo_api_url = "https://api.opencagedata.com/geocode/v1/json"
    # satelite_location_url = "https://tle.ivanstanojevic.me/api/tle/49044"
    # iss_location_api_url = "http://api.open-notify.org/iss-now.json"
    # # astronauts_list_url = "http://api.open-notify.org/astros.json"
    #
    # geo_params = {
    #     "key": geo_api_key,
    #     "q": geo_q,
    #     "pretty": 1,
    #     "no_annotations": 1
    # }
    #
    # URLS = []
    #
    # URLS.append((geo_api_url, geo_params))
    # URLS.append(satelite_location_url)
    # URLS.append(iss_location_api_url)
    # # URLS.append(astronauts_list_url)
    #
    # for url in URLS:
    #     r = None
    #     if not isinstance(url, tuple):
    #         r = await get_info_from_api(url)
    #     elif isinstance(url, tuple):
    #         r = await get_info_from_api(url[0], url[1])
    #         print(type(r))
    #         r = json.loads(r)
    #         print(type(r))
    #     print(r)

    params = await get_orbital_params(25544)

    get_cords(params)

asyncio.run(main())
# print(type((1,2)))