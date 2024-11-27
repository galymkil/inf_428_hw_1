# Use official Python image as base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose port for Elasticsearch (9200) and app (e.g., 5000 if using Flask)
EXPOSE 9200 5000

# Run the application
CMD ["python", "your_app.py"]

