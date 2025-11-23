FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY backend ./backend

# Collect static files
# RUN python backend/manage.py collectstatic --noinput

# Run Django server
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8002"]
