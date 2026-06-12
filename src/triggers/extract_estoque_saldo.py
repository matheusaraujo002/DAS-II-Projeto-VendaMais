import azure.functions as func
import logging
import pyodbc
import os
import time

app = func.Blueprint()

@app.timer_trigger(
    schedule="0 0 6 * * *",
    arg_name="timer",
    run_on_startup=False
)
def extract_estoque_saldo(timer: func.TimerRequest) -> None:

    # Banco Cris
    sql_server = os.getenv("SQL_SERVER_SOURCE")
    database = os.getenv("SQL_DATABASE_SOURCE")
    user = os.getenv("SQL_USER_SOURCE")
    password = os.getenv("SQL_PASSWORD_SOURCE")

    # Meu
    sql_server_dest = os.getenv("SQL_SERVER_456")
    database_dest = os.getenv("SQL_DATABASE_SOURCE_456")
    user_dest = os.getenv("SQL_DATABASE_USER")
    password_dest = os.getenv("SQL_DATABASE_PASSWORD")

    logging.info(
        f"Servidor origem: {sql_server}, Banco: {database}"
    )

    query = """
    SELECT
        id_estoque_saldo,
        id_produto,
        dt_referencia,
        qt_saldo,
        dt_inclusao,
        dt_atualizacao,
        nm_sistema_origem,
        cd_registro_origem
    FROM erp.estoque_saldo
    """

    tempos_execucao = []

    # Cris
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    # Meu
    conn_dest = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server_dest};"
        f"DATABASE={database_dest};"
        f"UID={user_dest};"
        f"PWD={password_dest};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:

        inicio = time.time()

        with pyodbc.connect(conn_str) as conn:

            cursor = conn.cursor()

            cursor.execute(query)

            rows = cursor.fetchall()
            #rows = cursor.fetchmany(5)
        tempo_extract = time.time() - inicio

        tempos_execucao.append(
            ("extract_estoque_saldo", tempo_extract)
        )

        logging.info(
            f"[entrega] {len(rows)} registros extraídos em {tempo_extract:.2f}s"
        )

        inicio_load = time.time()

        with pyodbc.connect(conn_dest) as conn:

            cursor_dest = conn.cursor()

            # verifica se a tabela existe
            cursor_dest.execute("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = 'dbo'
                AND TABLE_NAME = 'estoque_saldo'
            """)

            tabela_existe = cursor_dest.fetchone()[0]

            if tabela_existe == 0:

                logging.error(
                    "Tabela dbo.entrega não existe no banco destino."
                )

                return

            logging.info(
                "Tabela dbo.entrega encontrada."
            )

            # limpa os registros antigos
            cursor_dest.execute(
                "DELETE FROM dbo.estoque_saldo"
            )

            # habilita IDENTITY
            cursor_dest.execute(
                "SET IDENTITY_INSERT dbo.estoque_saldo ON"
            )

            for row in rows:

                cursor_dest.execute("""
                    INSERT INTO dbo.estoque_saldo(
                        id_estoque_saldo,
                        id_produto,
                        dt_referencia,
                        qt_saldo,
                        dt_inclusao,
                        dt_atualizacao,
                        nm_sistema_origem,
                        cd_registro_origem
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, row)

            cursor_dest.execute(
                "SET IDENTITY_INSERT dbo.estoque_saldo OFF"
            )

            conn.commit()

        tempo_load = time.time() - inicio_load

        tempos_execucao.append(
            ("load_entrega", tempo_load)
        )

        logging.info(
            f"[entrega] {len(rows)} registros carregados em {tempo_load:.2f}s"
        )

        for etapa, tempo in tempos_execucao:

            logging.info(
                f"Tempo {etapa}: {tempo:.2f}s"
            )

    except Exception as e:

        logging.error(
            f"[entrega] Erro: {e}"
        )

        raise