#1. basic information
FROM python:3.10-slim

#2. set workspace
WORKDIR /app

#3. install dependencies
RUN pip install flask

#4. copy app.py to /app dir in the container
COPY app.py /app/

#5. set environment variables
ENV PYTHONUNBUFFERED=1  
#let python print log immediately

#6. define the command to run in default when container starts
CMD ["python", "app.py"]