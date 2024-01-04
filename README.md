# Tools used
<li>Progmming language: Python</li>
<li>Backend web framework: Django and Django Rest Framework</li>
<li>Database: Postgres</li>
<li>Testing: pytest</li>
<li>Devops: Docker and Docker compose </li>


# Steps to run the application
### 1. docker build -t notesbackend .
### 2. docker-compose up
### 3. docker exec -it notesbackend-api  python src/manage.py migrate

## To run the tests
### docker exec -it notesbackend-api pytest src
