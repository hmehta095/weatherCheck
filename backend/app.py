import os
import httpx
from fastapi import FastAPI, Query,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = FastAPI()

# Allow browser JS requests from any local origin (for demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/weather")
async def weather(
    latitude: float = Query(...),
    longitude: float = Query(...)
):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current_weather": True}
    async with httpx.AsyncClient() as http_client:
        r = await http_client.get(url, params=params)
    data = r.json()
    print("Fetched data",  data)
    temp = data.get("current_weather", {}).get("temperature")

    if temp is None:
        raise HTTPException(status_code=404, detail="Temperature data not found")

    prompt = (
        f"Provide a short, friendly weather report for a location at latitude {latitude} and longitude {longitude}, "
        f"where the current temperature is {temp}°C."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )

    weather_report = response.choices[0].message.content.strip()

    # Return temperature and generated report
    return {"temperature": temp, "report": weather_report}
