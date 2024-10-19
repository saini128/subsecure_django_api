#Dockerfile
# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

RUN python manage.py collectstatic --noinput
# Run the application with Gunicorn and Uvicorn worker
CMD ["gunicorn", "worker_location_project.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]