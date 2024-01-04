# Tools used
Progmming language: Python </br>
Backend web framework: Django and Djangorestframework </br>
Database: Postgres </br>
Testing: pytest </br>
Devops: Docker and Docker compose </br>


# steps to run the application
### 1. docker build -t notesbackend .
### 2. docker-compose up
### 3. docker exec -it notesbackend-api  python src/manage.py migrate

## to run the tests
### docker exec -it notesbackend-api pytest src
