FROM python:3.8-slim

# Install required packages
RUN pip install boto3 pandas sqlalchemy pymysql

# Copy the Python script
COPY main.py /app/main.py

# Set the working directory
WORKDIR /app

# Set the entry point for the container
ENTRYPOINT ["python", "main.py"]