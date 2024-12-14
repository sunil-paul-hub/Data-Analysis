# Use a Python image as base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the application files to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
