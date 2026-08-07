import subprocess

def elegir_modelo():
    resultado = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True
    )

    lineas = resultado.stdout.strip().split("\n")

    modelos = []

    for linea in lineas[1:]:
        if linea.strip():
            modelo = linea.split()[0]
            modelos.append(modelo)

    if not modelos:
        print("No se encontraron modelos de Ollama.")
        return None

    print("\nModelos disponibles:\n")

    for i, modelo in enumerate(modelos, 1):
        print(f"{i}. {modelo}")

    while True:
        try:
            opcion = int(input("\nElige modelo: "))

            if 1 <= opcion <= len(modelos):
                elegido = modelos[opcion - 1]
                print(f"\nModelo seleccionado: {elegido}")
                return elegido

        except ValueError:
            pass

        print("Opción no válida.")


if __name__ == "__main__":
    elegir_modelo()