# Use a lightweight Python image
FROM python:3.12-slim

# Set the working direy inside the container
WORKDIR /app

# Install system dependenciessssss
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "backendpart.wsgi:application", "--bind", "0.0.0.0:8000"]
