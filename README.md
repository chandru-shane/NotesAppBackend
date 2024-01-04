# Tools used
Progmming language: Python
Backend web framework: Django and Djangorestframework
Database: Postgres
Testing: pytest
Devops: Docker and Docker compose


# steps to run the application
### 1. docker build -t notesbackend .
### 2. docker-compose up
### 3. docker exec -it notesbackend-api  python src/manage.py migrate

## to run the tests
### docker exec -it notesbackend-api pytest src
