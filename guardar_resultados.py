
import json
from datetime import datetime, timezone
from pymongo import MongoClient

cliente = None

try:
    with open("resultados_netflix.json", "r", encoding="utf-8") as archivo:
        resultados = json.load(archivo)

    cliente = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000
    )
    cliente.admin.command("ping")

    db = cliente["netflix"]
    coleccion = db["resultados_procesamiento"]

    documento = {
        **resultados,
        "fecha_procesamiento": datetime.now(timezone.utc)
    }

    resultado = coleccion.insert_one(documento)

    print("Resultados guardados correctamente en MongoDB.")
    print("ID:", resultado.inserted_id)
    print("Documentos almacenados:", coleccion.count_documents({}))

except Exception as error:
    print("Error:", error)

finally:
    if cliente is not None:
        cliente.close()
