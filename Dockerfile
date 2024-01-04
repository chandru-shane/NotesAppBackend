# Use an official Python runtime as a base image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /code

# Copy the project requirements file into the container
COPY requirements.txt requirements.txt

# Install project dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
# Copy the project code into the container
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

# Define the command to run on container start
# CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
