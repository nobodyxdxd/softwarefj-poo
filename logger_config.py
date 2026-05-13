import logging  # importa el módulo o símbolo necesario

logger = logging.getLogger("SoftwareFJ")  # asigna un valor a una variable o atributo
logger.setLevel(logging.INFO)  # ejecuta la instrucción correspondiente

if not logger.handlers:  # evalúa una condición para decidir el flujo
    formatter = logging.Formatter(  # asigna un valor a una variable o atributo
        "%(asctime)s - %(levelname)s - %(message)s"  # ejecuta la instrucción correspondiente
    )  # ejecuta la instrucción correspondiente

    file_handler = logging.FileHandler("sistema.log", encoding="utf-8")  # ejecuta la instrucción correspondiente
    file_handler.setLevel(logging.INFO)  # ejecuta la instrucción correspondiente
    file_handler.setFormatter(formatter)  # ejecuta la instrucción correspondiente
    logger.addHandler(file_handler)  # ejecuta la instrucción correspondiente
