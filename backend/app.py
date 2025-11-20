import os
import httpx
from fastapi import FastAPI, Query,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

app = FastAPI()

# Allow browser JS requests from any local origin (for demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/weather")
async def weather(
    latitude: float = Query(...),
    longitude: float = Query(...)
):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current_weather": True}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
    data = r.json()
    temp = data.get("current_weather", {}).get("temperature")
    return {"temperature": temp}
