FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1


COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .


EXPOSE 31337


CMD ["gunicorn", "-b", "0.0.0.0:31337", "main:app"]
