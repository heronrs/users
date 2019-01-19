# Users API

Simples API CRUD para cadastro de usuários

Desenvolvida em python, utilizando flask e extensões

A aplicação suporta o inject de variáveis de ambiente através de um arquivo .env no root do projeto.

    Variáveis de ambiente necessárias:

        FLASK_ENV(obrigatório) - Ambiente (development, production, staging, etc)
        FLASK_APP(obrigatório) - Nome do app ("api")
        FLASK_DEBUG(obrigatório) - 1 ou 0
        MONGODB_URI(brigatório) - Mongo conexion string na forma "mongodb://user:pass@db:27017/api"
        SECRET_KEY(obrigatório) - String utilizada internamente pelo Flask p/ controle de sessão, csrf, etc
        LOG_LEVEL(opcional) - Nível do Log, default INFO

- Documentação: [API Blueprint](./api.apib), [Html](./docs.html), [Postman](./API.postman_collection.json)

- Requisitos para rodar local: [Docker](https://docs.docker.com/install/), [Docker Compose](https://docs.docker.com/compose/) e [Python 3.6 +](https://www.python.org/downloads/) para desenvolvimento

- Iniciar ambiente local:
    
        $/users: sudo docker-compose up --build -d
        $/users: firefox localhost:8000/api/v1/users

- Rodar os testes:

        $/users: sudo docker-compose run api sh -c "find -name '*.pyc' -delete && pytest -v"

