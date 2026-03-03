# 1. Base image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application code
COPY app.py /app/

# 5. Set environment variables
ENV PYTHONUNBUFFERED=1

# 6. Define default command
CMD ["python", "app.py"]
