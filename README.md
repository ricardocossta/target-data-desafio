# Desafio Target-Data

## Tecnologias usadas:

 - Python (Flask)
 - HTML
 - CSS
 - JavaScript
 - Bootstrap
 - Mongodb
 - ElasticSearch
 
## Como rodar o projeto:

 - Clone o projeto
 - Abra o terminal na pasta raiz do projeto
 - Execute o seguinte comando: `docker compose up`
 -  Aguarde o docker finalizar o pull das imagens e startar o projeto
 - Coloque o arquivo CSV dos estabelecimentos dentro da pasta **massa_dados_estabelecimentos**, o arquivo deve ter exatamente o nome **dados.csv**
 - Execute o comando: `python .\massa_dados_estabelecimentos\app.py` para semear a base de dados do **MongoDB** e do **ElasticSearch**
 - Ao finalizar a inserção de dados, a aplicação pode ser testada entrando no endereço **http://localhost:5000/**
