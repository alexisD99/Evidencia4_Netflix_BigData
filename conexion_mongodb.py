
print("Iniciando prueba de MongoDB...")

from pymongo import MongoClient
from datetime import datetime, timezone

try:
    cliente = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000
    )

    cliente.admin.command("ping")
    print("Conexion con MongoDB exitosa")

    db = cliente["netflix"]
    comentarios = db["comentarios"]

    documento = {
        "contenido": "Me gustan las peliculas y series de Netflix",
        "fuente": "prueba_integracion",
        "fecha_procesamiento": datetime.now(timezone.utc)
    }

    resultado = comentarios.insert_one(documento)

    print("Documento guardado:", resultado.inserted_id)
    print("Total de documentos:", comentarios.count_documents({}))

    cliente.close()

except Exception as error:
    print("Error:", error)
