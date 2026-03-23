# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (layer caching benefit)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]