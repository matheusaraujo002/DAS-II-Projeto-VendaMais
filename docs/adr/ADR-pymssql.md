# ADR-pymssql: Escolha de Biblioteca Python para Acesso ao Banco de Dados

**Status:** Aceito  
**Data:** 27/05/2026  
**Autores:** Guilherme da Costa, Matheus de Araújo e Yohann / Engenharia de Software

---

## Contexto

Foi realizada uma Prova de Conceito (PoC) com o objetivo de comparar o desempenho de bibliotecas Python utilizadas para acesso a banco de dados.

O cenário da análise consistiu em:
- Utilizar o mesmo banco de dados;
- Executar o mesmo comando `SELECT`;
- Trabalhar com a mesma volumetria de dados;
- Medir o tempo necessário para consultar e carregar os registros em memória.

As bibliotecas avaliadas foram:
- `pymssql`
- `pyodbc`

Os testes foram executados duas vezes para cada biblioteca, realizando posteriormente o cálculo da média de tempo.

### Resultados obtidos

| Biblioteca | Teste 1 | Teste 2 | Média |
|---|---|---|---|
| pymysql | 0.3606s | 0.3034s | 0.3320s |
| pyodbc | 0.6553s | 0.4903s | 0.5728s |

O objetivo principal da análise foi identificar qual biblioteca apresenta melhor desempenho para operações de leitura em um ambiente utilizando MySQL.

---

## Decisão

A biblioteca escolhida para utilização no cenário analisado foi o `pymssql`.

A decisão foi baseada nos resultados da PoC, onde o `pymssql` apresentou menor tempo médio de execução em comparação ao `pyodbc`.

O `pymssql` será adotado para operações de acesso ao banco MySQL quando o foco principal for:
- desempenho;
- menor latência;
- comunicação nativa com o banco.

---

## Consequências

(+) Melhor desempenho em consultas `SELECT`

(+) Menor tempo médio de resposta

(+) Comunicação nativa com MySQL, reduzindo overhead

(-) Dependência específica do MySQL

(-) Menor portabilidade para outros bancos compatíveis com ODBC

---

## Alternativas rejeitadas

- `pyodbc`: rejeitado por apresentar maior tempo médio de execução devido à camada intermediária ODBC.

- `SQLAlchemy ORM`: não utilizado pois o foco da PoC era comparar bibliotecas de acesso direto ao banco e não ORMs.

- `psycopg2`: não utilizado porque a PoC foi executada em ambiente MySQL, enquanto a biblioteca é voltada para PostgreSQL.

---

## Links

- Substitui: Nenhum

- Relacionado: PoC de benchmark entre `pymssql` e `pyodbc`

- Evidências:
  - Logs de execução da Azure Function
  - Resultados médios coletados durante os testes
  - Benchmark realizado com consultas `SELECT` em mesma tabela e volumetria de dados