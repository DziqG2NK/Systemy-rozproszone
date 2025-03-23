import httpx
import asyncio
import json
from datetime import datetime
from sgp4.api import Satrec
from sgp4.api import jday

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

    response = json.loads(s=response)

    orbital_params = {
    "date": response["date"],
    "line_1": response["line1"],
    "line_2": response["line2"]
    }

    return orbital_params


# async def get_satellite_location(json_response: dict):



async def main():
    geo_api_key = "e2357fc9ddfb401bade0d477f1f0ce7e"
    geo_q = "52.5432379+13.41421330"
    geo_q = "52.5432379%2C+13.4142133"

    geo_api_url = "https://api.opencagedata.com/geocode/v1/json"
    satelite_location_url = "https://tle.ivanstanojevic.me/api/tle/49044"
    iss_location_api_url = "http://api.open-notify.org/iss-now.json"
    # astronauts_list_url = "http://api.open-notify.org/astros.json"

    geo_params = {
        "key": geo_api_key,
        "q": geo_q,
        "pretty": 1,
        "no_annotations": 1
    }

    URLS = []

    URLS.append((geo_api_url, geo_params))
    URLS.append(satelite_location_url)
    URLS.append(iss_location_api_url)
    # URLS.append(astronauts_list_url)

    for url in URLS:
        r = None
        if not isinstance(url, tuple):
            r = await get_info_from_api(url)
        elif isinstance(url, tuple):
            r = await get_info_from_api(url[0], url[1])
            print(type(r))
            r = json.loads(r)
            print(type(r))
        print(r)

asyncio.run(get_orbital_params(25544))
# print(type((1,2)))