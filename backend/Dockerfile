FROM python:3.11-slim
WORKDIR /app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

# Above command didn't worked so, using individual install
RUN pip install fastapi 
RUN pip install httpx
RUN pip install python-dotenv
RUN pip install pydantic
RUN pip install uvicorn[Standard]
RUN pip install openai

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]