#Use an official Python runtime as a parent image
FROM python:3.12-slim

#Set the working directory in the container
WORKDIR /app

#Copy requirements.txt
COPY requirements.txt ./

#Install project dependencies
RUN pip install -r requirements.txt

#Copy the rest of the application code into the container
COPY . .

EXPOSE 8080

#Run application.py when the container launches
CMD ["gunicorn", "application:application", "--bind", "0.0.0.0:8080"]