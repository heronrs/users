# Desafio Backend

API desenvolvida como parte do processo seletivo da Mira Educação

Desenvolvida em python, utilizando flask e extensões

- URL Heroku: https://miraed-challenge.herokuapp.com/api/v1/users/

- Documentação: [API Blueprint](./api.apib), [Html](./docs.html), [Postman](./API.postman_collection.json)

- Requisitos para rodar local: [Docker](https://docs.docker.com/install/), [Docker Compose](https://docs.docker.com/compose/) e [Python 3.6 +](https://www.python.org/downloads/) para desenvolvimento

- Instalar dependências localmente:
        
        $/miraed_challenge: pip install -r requirements_dev.txt

- Iniciar ambiente local:
    
        $/miraed_challenge: sudo docker-compose up -d
        $/miraed_challenge: firefox localhost:8000/api/v1/users

- Rodar os testes:

        $/miraed_challenge: sudo docker-compose run api sh -c "find -name '*.pyc' -delete && pytest -v"

