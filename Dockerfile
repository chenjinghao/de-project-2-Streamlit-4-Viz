# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run streamlit when the container launches
# Cloud Run expects the app to listen on the environment variable PORT
CMD streamlit run home.py --server.port=${PORT:-8501} --server.address=0.0.0.0
