# Users API

Simples API CRUD para cadastro de usuários

Desenvolvida em python, utilizando flask e extensões

- Documentação: [API Blueprint](./api.apib), [Html](./docs.html), [Postman](./API.postman_collection.json)

- Requisitos para rodar local: [Docker](https://docs.docker.com/install/), [Docker Compose](https://docs.docker.com/compose/) e [Python 3.6 +](https://www.python.org/downloads/) para desenvolvimento

- Iniciar ambiente local:
    
        $/users: sudo docker-compose up --build -d
        $/users: firefox localhost:8000/api/v1/users

- Rodar os testes:

        $/users: sudo docker-compose run api sh -c "find -name '*.pyc' -delete && pytest -v"

