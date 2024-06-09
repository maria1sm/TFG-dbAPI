# Use an official Python runtime as a parent image
FROM python:3.10-slim AS build

COPY requirements.txt /opt/app/requirements.txt
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update Pip to the latest version
RUN pip install --upgrade pip

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]