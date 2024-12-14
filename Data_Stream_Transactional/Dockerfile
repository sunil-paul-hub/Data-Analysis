# Use Python 3.9 image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python app files to the container
COPY . /app

# Install required dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
