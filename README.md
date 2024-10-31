# P6-Snelf

## Sobre a ferramenta

O SNELF é uma plataforma para detecção de disparidades de preços em compras públicas. O objetivo é auxiliar na auditoria de notas fiscais relacionadas a compras, e verificar possíveis fraudes. A ferramenta permite a importação de um CSV, nesse caso uma base de dados de medicamentos, para que possa ser treinado um modelo de predição que associe medicamentos iguais porém que possuem nomes diferentes nas notas fiscais, dado que o campo de descrição da nota fiscal é livre.
Assim, quando importamos a base de dados, o modelo já classifica cada registro com um código diferente, que relaciona os mesmos medicamentos porém com nomes distintos. Após isso, podem ser realizadas buscas por nomes de medicamentos, que retornam um conjunto de compras de notas fiscais. Na tela podemos observar dados sobre o conjunto de dados requisitado, como média, moda, mediana, uma tabela com todas as compras retornadas, e um gráfico boxplot com a variável preço no tempo. Também conseguimos excluir algum registro do cálculo se for desejado, dando mais flexibilidade para quem está fazendo a análise.

### Arquitetura e tecnologias
O SNELF foi desenvolvido utilizando arquitetura REST, utilizando o framework Python FastAPI, que serve para criar APIs de forma bem simples. Dessa forma, conseguimos disponibilizar nossos endpoints para acesso da interface. O frontend foi desenvolvido utilzando ReactJS. Por fim, o banco de dados relacional utilizado foi o PostgreSQL.

Cabe ressaltar que, na pasta 'dumps do postgresql', existirão diversas versões do banco de dados, caso seja necessário restaurar alguma versão específica.

## Como utilizar?

### Passos
#### 1. Clonar o repositório em uma pasta dentro de um WSL
#### 2. Instalar o docker
    Acessar https://docs.docker.com/engine/install/ubuntu/ e seguir o passo-a-passo
#### 3. Instalar o docker-compose
    Acessar https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04 e seguir o passo-a-passo
#### 4. Acessar a pasta snelf
    Digitar o comando 'cd snelf' e apertar a tecla Enter
#### 5. Realizar o build das imagens do repositório (docker-compose.yml)
    sudo docker-compose build
#### 6. Subir containers do repositório
    sudo docker-compose up
#### 7. Iniciar o repositório
    sudo docker-compose start
#### 8. Configurar conexão com SGBD (sistema gerenciador de banco de dados)
##### 8.1 Baixar o DBeaver (sistema gerenciador de múltiplos tipos de bancos de dados)
##### 8.2 Criar uma nova conexão no DBeaver, com os seguintes dados:
    Host: localhost
    Database: testejp
    Port: 5432
    Username: testejp
    Password: testejp
##### 8.3 Acessar o site
    Acessar localhost:7767 para abrir a página inicial do Snelf.

#### 9. Primeiro acesso ao sistema
Caso seja seu primeiro acesso ao sistema, seguir todos os passos desta seção.
##### 9.1 Inserir arquivo CSV no sistema
- Acessar a opção "Importar Base de Transações"
- Clicar no botão "UPLOAD CSV"
- O arquivo exemplo que deverá ser importado está na pasta snelf/produtos_farmaceuticos.csv
- Após feito o upload, clicar no botão "IMPORTAR"

##### 9.2 Treinar o modelo, para clusterização de classes de medicamentos
- Após realizada a importação do csv, acessar a opção "Atualizar Treinamento do Modelo"
- Clicar no botão "TREINAR MODELO"

##### 9.3 Pesquisar transações
- Acessar a opção "Buscar Produtos"
- Selecionar o modo de busca (Produto ou CLEAN)
- Inserir o nome do produto ou clean (as buscas podem conter strings parciais)
- O usuário pode baixar os resultados como PDF ou Excel, visualizar transações passadas para os medicamentos, as principais estatísticas das transações retornadas e um gráfico box-plot considerando os preços praticados para as transações retornadas


#### Parar o docker compose:
Para parar o container, basta rodar o comando 'sudo docker-compose stop'
