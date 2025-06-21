# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY gcp_requirements.txt .
RUN pip install --no-cache-dir -r gcp_requirements.txt

# Copy application code
COPY gcp_app/ ./gcp_app/
COPY cpr_data/ ./cpr_data/

# Create a non-root user
RUN useradd -m -u 1000 streamlit
RUN chown -R streamlit:streamlit /app
USER streamlit

# Expose port
EXPOSE 8080

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the application
CMD ["streamlit", "run", "gcp_app/app.py", "--server.port=8080", "--server.address=0.0.0.0"] 