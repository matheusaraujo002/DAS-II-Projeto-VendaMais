import logging
import azure.functions as func

app = func.FunctionApp()

# Importa triggers para registrar as functions no app
from triggers.extract_cliente import app as extract_cliente
from triggers.extract_entrega import app as extract_entrega
from triggers.extract_pedido import app as extract_pedido

# Registrar as azure functions
app.register_functions(extract_cliente)
app.register_functions(extract_entrega)
app.register_functions(extract_pedido)
logging.info("Azure Function App inicializado.")