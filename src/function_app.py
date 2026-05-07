import logging
import azure.functions as func

app = func.FunctionApp()

# Importa triggers para registrar as functions no app
from triggers.extract_cliente import app as extract_trigger
from triggers.extract_entrega import app as extract_trigger
from triggers.extract_pedido import app as extract_trigger

app.register_functions(extract_trigger)
logging.info("Azure Function App inicializado.")