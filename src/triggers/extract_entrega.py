import azure.functions as func
import logging
import pyodbc
import os
import time

app = func.Blueprint()

@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
def extract_entrega(timer: func.TimerRequest) -> None:

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    database = os.getenv("SQL_DATABASE_SOURCE")
    user = os.getenv("SQL_USER_SOURCE")
    password = os.getenv("SQL_PASSWORD_SOURCE")

    logging.info(
        f"Servidor: {sql_server}, Banco: {database}, Usuario: {user}"
    )

    query = "SELECT * FROM erp.pedido"

    tempos_execucao = []

    # String de conexão ODBC
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

    try:

        # Executa 2 vezes
        for i in range(2):

            logging.info(f"Iniciando teste {i + 1} com pyodbc")

            # Marca início
            inicio = time.perf_counter()

            # Abre conexão
            with pyodbc.connect(conn_str) as conn:

                cursor = conn.cursor()

                # Executa SELECT
                cursor.execute(query)

                # Carrega TODAS as linhas em memória
                rows = cursor.fetchall()

            # Marca fim
            fim = time.perf_counter()

            # Calcula duração
            duracao = fim - inicio

            tempos_execucao.append(duracao)

            logging.info(
                f"Teste {i + 1} concluído - "
                f"{len(rows)} linhas carregadas em "
                f"{duracao:.4f} segundos"
            )

        # Média
        tempo_medio = sum(tempos_execucao) / len(tempos_execucao)

        logging.info(
            f"Tempo médio de SELECT: {tempo_medio:.4f} segundos"
        )

    except Exception as e:
        logging.error(f"Erro ao ler erp.pedido: {str(e)}")
        raise