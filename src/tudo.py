import azure.functions as func
import logging
import pyodbc
import os
import time

app = func.Blueprint()

# Ordem de carga
TABELAS_CARGA = [
    "categoria_produto",
    "regiao",
    "transportadora",
    "representante",
    "produto",
    "cliente",
    "pedido",
    "pedido_item",
    "titulo_receber",
    "entrega",
    "estoque_saldo",
    "estoque_movimentacao"
]

# Ordem inversa para DELETE
TABELAS_DELETE = [
    "estoque_movimentacao",
    "estoque_saldo",
    "entrega",
    "titulo_receber",
    "pedido_item",
    "pedido",
    "cliente",
    "produto",
    "representante",
    "transportadora",
    "regiao",
    "categoria_produto"
]

@app.timer_trigger(
    schedule="0 0 6 * * *",
    arg_name="timer",
    run_on_startup=False
)
def tudo(timer: func.TimerRequest) -> None:

    logging.info("Iniciando sincronização completa")

    conn_source = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('SQL_SERVER_SOURCE')};"
        f"DATABASE={os.getenv('SQL_DATABASE_SOURCE')};"
        f"UID={os.getenv('SQL_USER_SOURCE')};"
        f"PWD={os.getenv('SQL_PASSWORD_SOURCE')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    conn_dest = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('SQL_SERVER_456')};"
        f"DATABASE={os.getenv('SQL_DATABASE_SOURCE_456')};"
        f"UID={os.getenv('SQL_DATABASE_USER')};"
        f"PWD={os.getenv('SQL_DATABASE_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:

        with pyodbc.connect(conn_source) as origem, \
             pyodbc.connect(conn_dest) as destino:

            cursor_origem = origem.cursor()
            cursor_destino = destino.cursor()

            logging.info("Iniciando limpeza das tabelas")

            # DELETE
            for tabela in TABELAS_DELETE:

                try:

                    cursor_destino.execute(
                        f"DELETE FROM dbo.{tabela}"
                    )

                    logging.info(
                        f"dbo.{tabela} limpa"
                    )

                except Exception as e:

                    logging.warning(
                        f"Erro ao limpar dbo.{tabela}: {e}"
                    )

            destino.commit()

            logging.info("Iniciando carga")

            # CARGA
            for tabela in TABELAS_CARGA:

                inicio = time.time()

                logging.info(
                    f"Carregando dbo.{tabela}"
                )

                cursor_origem.execute(
                    f"SELECT * FROM erp.{tabela}"
                )

                rows = cursor_origem.fetchall()

                if not rows:

                    logging.warning(
                        f"erp.{tabela} sem registros"
                    )

                    continue

                # Descobre colunas da tabela destino
                cursor_destino.execute(f"""
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = 'dbo'
                    AND TABLE_NAME = '{tabela}'
                    ORDER BY ORDINAL_POSITION
                """)

                colunas = [
                    coluna[0]
                    for coluna in cursor_destino.fetchall()
                ]

                nomes_colunas = ", ".join(colunas)

                placeholders = ", ".join(
                    ["?"] * len(colunas)
                )

                insert_sql = f"""
                    INSERT INTO dbo.{tabela}
                    ({nomes_colunas})
                    VALUES ({placeholders})
                """

                # tenta habilitar IDENTITY
                try:

                    cursor_destino.execute(
                        f"SET IDENTITY_INSERT dbo.{tabela} ON"
                    )

                except:

                    pass

                for row in rows:

                    cursor_destino.execute(
                        insert_sql,
                        row
                    )

                # tenta desabilitar IDENTITY
                try:

                    cursor_destino.execute(
                        f"SET IDENTITY_INSERT dbo.{tabela} OFF"
                    )

                except:

                    pass

                destino.commit()

                tempo = time.time() - inicio

                logging.info(
                    f"{tabela}: "
                    f"{len(rows)} registros "
                    f"carregados em "
                    f"{tempo:.2f}s"
                )

        logging.info(
            "Sincronização concluída com sucesso"
        )

    except Exception as e:

        logging.error(
            f"Erro geral: {e}"
        )

        raise