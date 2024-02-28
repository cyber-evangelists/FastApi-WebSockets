FROM python:3.10.6

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.app.web_socket:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
