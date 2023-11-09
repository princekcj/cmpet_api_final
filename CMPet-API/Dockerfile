# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Create a virtual environment and activate it
RUN python -m venv venv
# Use the "bash" shell to activate the virtual environment and install dependencies
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip setuptools && \
    apt-get update && apt-get install -y default-libmysqlclient-dev pkg-config build-essential

RUN pip install -r requirements.txt

# Define environment variable
ENV DEBUG=false

# Expose the port Uvicorn will listen on
EXPOSE 80

# Define the command to start your FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]