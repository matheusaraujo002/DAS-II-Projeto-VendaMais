# Atividade EL - Azure Functions

## Objetivo

Desenvolver uma pipeline EL (Extract and Load) utilizando Azure Functions para copiar os dados do banco do professor para um banco Azure SQL Database.

## O que foi realizado

Foram criadas Azure Functions responsáveis por:

1. Extrair os dados do banco de origem.
2. Carregar os dados no banco de destino.
3. Sincronizar todas as tabelas do ERP.

## Tabelas sincronizadas

- categoria_produto
- regiao
- transportadora
- produto
- representante
- cliente
- estoque_saldo
- pedido
- pedido_item
- titulo_receber
- entrega
- estoque_movimentacao

## Tecnologias utilizadas

- Python
- Azure Functions
- Azure SQL Database
- pyodbc

## Evidências Banco 
![Estoque Movimentação](docs/images/estoque_movimentacao.png)
![Relacionamento](docs/images/relacionamento.png)

## Resultado

Os dados foram extraídos do banco do professor e carregados com sucesso no banco Azure SQL Database próprio utilizando Azure Functions.