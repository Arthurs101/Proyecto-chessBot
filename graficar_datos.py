import json
import matplotlib.pyplot as plt


def graficar_resultados(resultados_file):
    try:
        with open(resultados_file, 'r') as file:
            resultados = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No se encontraron resultados para graficar.")
        return

    labels = list(resultados.keys())
    values = list(resultados.values())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=['blue', 'green', 'gray'])
    plt.xlabel('Resultados')
    plt.ylabel('Cantidad de Juegos')
    plt.title('Resultados de los Juegos entre MinMax y DEEPQ')
    plt.show()

# Llamar a la función para graficar los resultados
graficar_resultados('resultados.json')