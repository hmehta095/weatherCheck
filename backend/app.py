import os
import httpx
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

Open_Meteo_URL = "https://api.open-meteo.com/v1/forecast"

async def get_current_temperature(lat: float, lon: float) -> tuple[float, str]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    async with httpx.AsyncClient() as http_client:
        r = await http_client.get(Open_Meteo_URL, params=params, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream weather API error")
    data = r.json()
    if "current_weather" not in data:
        raise HTTPException(status_code=500, detail="No current weather data")
    temp = data["current_weather"]["temperature"]
    unit = "°C"  
    return temp, unit

