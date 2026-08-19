FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 8000

# Run migrations and start gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn skssf_portal.wsgi:application --bind 0.0.0.0:8000"]
