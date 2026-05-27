import azure.functions as func
import logging
import pymssql
import os
import time

app = func.Blueprint()

@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
def extract_entrega_pymssql(timer: func.TimerRequest) -> None:

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    database = os.getenv("SQL_DATABASE_SOURCE")
    user = os.getenv("SQL_USER_SOURCE")
    password = os.getenv("SQL_PASSWORD_SOURCE")

    logging.info(
        f"Servidor: {sql_server}, Banco: {database}, Usuario: {user}"
    )

    query = "SELECT * FROM erp.pedido"

    tempos_execucao = []

    try:
        # Executa o teste 2 vezes
        for i in range(2):

            logging.info(f"Iniciando teste {i + 1}")

            # Marca o tempo inicial
            inicio = time.perf_counter()

            # Abre conexão
            conn = pymssql.connect(
                server=sql_server,
                user=user,
                password=password,
                database=database,
                timeout=30,
                login_timeout=30
            )

            cursor = conn.cursor(as_dict=True)

            # Executa SELECT
            cursor.execute(query)

            # Carrega TODAS as linhas para memória
            rows = cursor.fetchall()

            # Marca tempo final
            fim = time.perf_counter()

            # Calcula duração
            duracao = fim - inicio

            tempos_execucao.append(duracao)

            logging.info(
                f"Teste {i + 1} concluído - "
                f"{len(rows)} linhas carregadas em "
                f"{duracao:.4f} segundos"
            )

            # Fecha conexão
            cursor.close()
            conn.close()

        # Calcula média
        tempo_medio = sum(tempos_execucao) / len(tempos_execucao)

        logging.info(
            f"Tempo médio de SELECT: {tempo_medio:.4f} segundos"
        )

    except Exception as e:
        logging.error(f"Erro ao ler erp.pedido: {str(e)}")
        raise