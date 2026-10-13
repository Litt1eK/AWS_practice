FROM python:3.12.0-alpine
WORKDIR /app
COPY app.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]