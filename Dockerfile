# Use a lightweight Python base image compatible with Docker Desktop for Windows
FROM python:3.11-slim

# Set sane defaults for environment variables that the app reads.
ENV UPLOAD_FOLDER=/uploads \
    SECRET_KEY=dev-secret \
    AUTH_MODE=none \
    UPLOAD_TOKEN=changeme \
    ADMIN_PASSWORD=password \
    PORT=5000

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Ensure uploads directory exists and is writable
RUN mkdir -p "$UPLOAD_FOLDER" && \
    chown -R root:root "$UPLOAD_FOLDER"

# Expose the port configured by the PORT environment variable
EXPOSE $PORT

# Default command to start the Flask app
CMD ["python", "app.py"]
