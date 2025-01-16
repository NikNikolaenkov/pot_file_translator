FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

ENV PYTHONPATH=/app
ENV FLASK_APP=src/main.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"] 