# Sample Project - Data Engineer - GCP

Este projeto contém uma solução para o desafio Engenheiro de Dados que consiste em criar processo de Ingestão de Dados com Google Cloud Platform e Python SDK.

## Requisitos:
- Projeto GCP
- Chave Json do Usuário Proprietário do Projeto
+ Conta com os privilégios(Papéis):
    + Administrador do Dataflow
    + Administrador do Composer
    + Administrador do BigQuery
    + Administrador de Ambiente e Objetos do Storage
    + Administrador do Compute
    + Trabalhador do Dataflow
    + Usuário da Conta de Serviço



## Ambiente:
+ Google Cloud Platform:
    + Cloud Storage (Data Lake).
    + Dataflow com Python SDK (Ingestão de Dados).
    + BigQuery (Data Warehouse).
    + Data Studio (Data Visualization).
    + Cloud Shell (Infraestrutura).
- Python.
- Apache Beam.

## Arquitetura Proposta:
![](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/blob/main/diagrams/arquitetura_proposta.png)

#### Data Lake
- Para o Data Lake foi escolhido o Cloud Storage pois o armazenamento é em nuvem, pelo custo benefício e alta segurança dos dados. 
#### ETL
- Para o processo de ETL conforme requisitado, foi utilizado o Dataflow com Python JDK, o pipeline criado faz a leitura dos 3 arquivos no bucket criado no Cloud Storage (Data Lake) e após alguns tratamentos, cria as tabelas no BigQuery, neste caso são criadas três tabelas, uma para cada .csv.
#### Data Warehouse
- Para Data Warehouse foi escolhido o BigQuery, além de comportar processamento de grandes volumes de dados, provê um excelente ambiente para análises escalonáveis.
#### Data Visualization
- Para realizar a Visualização dos Dados, foi escolhido o Data Studio, ferramenta totalmente integrada e com suporte para diversos datasources.

## Modelo Conceitual dos Dados:
![](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/blob/main/diagrams/modelagem_conceitual.png)

Cada arquivo foi representado como uma entidade:
- tb_price_quote (Tabela Dimensional) [price_quote.csv](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/blob/main/data_files/price_quote.csv): Contém os preços das cotações dos fornecedores.
- tb_bill_materiais (Tabela Fato) [bill_of_materials.csv](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/blob/main/data_files/bill_of_materials.csv) : Contém a registros sobre os tubos e seus compenentes que foram selecionados.
- tb_components (Tabela Dimensional) [comp_boss.csv](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/blob/main/data_files/comp_boss.csv): Contém os detalhes dos componentes utilizados ou não na cotação de algum tubo.


# Instruções para Implementação

## Configurar Credenciais do GCP:
   Configure o gsutil para utilizar as credencias da conta GCP SDK, digite no Cloud Shell o comando:
```python
gcloud auth login
```
Ao digitar o comando, será carregado um link para gerar uma chave de autenticação, acesse o link, autentique com sua conta GCP, copie a chave e cole no Cloud Shell



## Criação Bucket (Data Lake):
   Estrutura do Dataset:
![](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/blob/main/diagrams/estrutura_dataset_bigquery.png)

  Para criar o Bucket, digite o comando para criar o bucket:
```python
gsutil mb -p desafio-engenheiro-de-dados -c STANDARD -l US-EAST1 -b on gs://bucket-desafio-engenheiro-dados-data-lake
```
Sintaxe: gsutil mb -p **ID DO PROJETO GCP** -c **CLASSE DE ARMAZENAMENTO** -l **REGIÃO** -b on gs://**NOME DO BUCKET**

## Upload dos Arquivos no Data Lake:
   Acesse o Bucket criado e faça upload dos arquivos no Data lake criado bill_of_materials.csv, comp_boss.csv e price_quote.csv localizados no diretório data_files [link do diretório](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/tree/main/data_files).

## Instalação de Pacotes e Configuração do Ambiente Virtual:
Execute o comando abaixo:
```python
virtualenv -p python3 venv 
source venv/bin/activate 
pip install 'apache-beam[gcp]' 
```
Feito isso, instale cada pacote:
```python
pip install regex
```
```python
pip install google-cloud-storage
```

No terminal do Cloud Shell, crie a pasta para armazenar os recursos para criação dos pipelines com o comando:
```python
mkdir resources
cd resources/
```
 Acesse o Editor do Cloud Shell, faça upload de todos o arquivos localizados na pasta scripts_and_support_files na pasta "resources". [link do diretório](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/tree/main/scripts_and_support_files).

## Baixando a chave json do usuário:
+ Acesse https://console.cloud.google.com/iam-admin/serviceaccounts 
    + Na aba **Ações**, clique nas **reticências** > **Gerenciar Chaves** > Clique no botão **ADICIONAR CHAVE** > **Criar Nova Chave** > Selecione **JSON** e clique no botão **criar**.
O arquivo json da chave será baixada automaticamente para seu computador, acesse o Editor do Cloud Shell e faça upload do arquivo na pasta "resources".

## Criação do Dataset no BigQuery(Data Warehouse):
No Terminal, utilize o comando abaixo para criar o dataset "**industrial_machine_product_data**":
```python
    python3 create_bigquery_dataset.py
```
## Estrutura do pipeline:
   ![](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/blob/main/diagrams/diagrama_pipeline.png)
_Os dados não processados são armazenados no Cloud Storage, o Python sdk extraí o arquivo que é processado pelo Dataflow e inserido no BigQuery para que sejam construídas as Views para consumo do Data Studio ou alguma Data Visualization Tool._


## Execução dos Jobs:
   Para executar os pipelines no Dataflow para que os arquivos sejam ingeridos do Cloud Storage(Data Lake) para o BigQuery(Data Warehouse), utilize os comandos abaixo para cada arquivo:
```python
python3 job_load_bill_of_materials.py
```
```python
python3 job_load_price_quote.py
```
```python
python3 job_load_comp_boss.py
```
Feito isso, serão criadas três tabelas no BigQuery:
- tb_price_quote (price_quote.csv)
- tb_bill_materiais (bill_of_materials.csv)
- tb_components (comp_boss.csv)

## Criação das Views BigQuery:
### Abaixo os códigos de duas Views simples para consolidar a disponibilidade de consumo dos dados pelo Data Studio a partir do BigQuery após a execução do processo ETL:
- Top 10 Fornecedores por Quantidade de Cotação
```sql
SELECT  tpq.supplier AS fornecedor,
        COUNT(tpq.tube_assembly_id) AS quantidade
  FROM  `desafio-engenheiro-de-dados.industrial_machine_product_data.tb_price_quote` tpq
 GROUP BY tpq.supplier
 ORDER BY quantidade_cotacao DESC
 LIMIT 10
```
- Top 10 Tubos por Quantidade de Cotação
```sql
SELECT tpq.tube_assembly_id AS tubo,
       SUM(tpq.quantity) as quantidade
  FROM `desafio-engenheiro-de-dados.industrial_machine_product_data.tb_price_quote` tpq
group by tube_assembly_id
 ORDER BY quantidade DESC
Limit 10
```

## Data Visualization:
### Foram criados os seguintes relatórios:
- Top 10 Fornecedores por Quantidade Cotação
- Top 10 Tubos por Quantidade Cotação

Ambos estão no diretório **data_visualization/** e podem ser visualizados [Clicando aqui](https://github.com/chagasfelipe/desafio-engenheiro-de-dados/tree/main/data_visualization)


## Próximos Passos (Melhorias)
- Execução Automática dos Jobs com Cloud Functions a partir de inserção de novos registros no data lake.
- Criar um Job Ariflow para que o pipeline seja executado de forma agendada.
- Melhoria do código python.
- Se aprofundar nos conceitos de negócio da demanda para novos insights, melhoria no processo de transformação dos dados.
