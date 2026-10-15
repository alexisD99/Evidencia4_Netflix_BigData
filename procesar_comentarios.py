
import json
import re
from collections import Counter

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower

print("Iniciando procesamiento de comentarios de Netflix...")

spark = (
    SparkSession.builder
    .appName("NetflixBigDataETL")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

try:
    # 1. EXTRACCION: leer los comentarios desde HDFS
    ruta = "hdfs://namenode:9000/input/*.txt"
    rdd = spark.sparkContext.textFile(ruta)

    total_comentarios = rdd.count()
    print("Total de comentarios:", total_comentarios)

    # 2. TRANSFORMACION CON RDD: contar las palabras
    palabras = (
        rdd.flatMap(
            lambda linea: re.findall(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ]+\b", linea.lower())
        )
        .map(lambda palabra: (palabra, 1))
        .reduceByKey(lambda a, b: a + b)
    )

    palabras_top = palabras.takeOrdered(
        10, key=lambda elemento: -elemento[1]
    )

    print("\nLas 10 palabras mas frecuentes:")
    for palabra, cantidad in palabras_top:
        print(f"{palabra}: {cantidad}")

    # 3. TRANSFORMACION CON DATAFRAME Y SQL
    df = spark.createDataFrame(
        rdd.map(lambda texto: (texto,)),
        ["contenido"]
    )

    df.createOrReplaceTempView("comentarios")

    total_con_peliculas = spark.sql("""
        SELECT COUNT(*) AS total
        FROM comentarios
        WHERE LOWER(contenido) LIKE '%películas%'
    """).first()["total"]

    print("\nTotal de comentarios:", df.count())
    print("Comentarios que contienen 'películas':", total_con_peliculas)

    # 4. PREPARAR RESULTADOS PARA LA CARGA EN MONGODB
    resultados = {
        "proyecto": "Netflix Big Data",
        "total_comentarios": total_comentarios,
        "total_palabras": palabras.map(lambda x: x[1]).sum(),
        "comentarios_con_peliculas": total_con_peliculas,
        "palabras_frecuentes": [
            {"palabra": palabra, "cantidad": cantidad}
            for palabra, cantidad in palabras_top
        ]
    }

    with open("/tmp/resultados_netflix.json", "w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, ensure_ascii=False, indent=2)

    print("\nResultados guardados en /tmp/resultados_netflix.json")

finally:
    spark.stop()
