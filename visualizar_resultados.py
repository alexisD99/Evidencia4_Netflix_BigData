
import json
import matplotlib.pyplot as plt

with open("resultados_netflix.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

palabras = datos["palabras_frecuentes"]
nombres = [item["palabra"] for item in palabras]
cantidades = [item["cantidad"] for item in palabras]

plt.figure(figsize=(10, 6))
plt.barh(nombres[::-1], cantidades[::-1])
plt.xlabel("Número de apariciones")
plt.ylabel("Palabras")
plt.title("10 palabras más frecuentes en comentarios de Netflix")
plt.tight_layout()
plt.savefig("grafico_palabras_netflix.png", dpi=150)
plt.show()

print("Gráfico guardado en grafico_palabras_netflix.png")
