RUTA_CSV = "paises.csv"
ENCABEZADO_CSV = "nombre,poblacion,superficie,continente"


# ============================================================
# VALIDACIONES
# ============================================================

def validar_no_vacio(texto):
    """Devuelve True si el texto, sin espacios al inicio/fin, no está vacío."""
    return texto.strip() != ""


def pedir_texto_no_vacio(mensaje):
    """Pide texto por consola hasta que el usuario ingrese algo no vacío."""
    while True:
        texto = input(mensaje).strip()
        if validar_no_vacio(texto):
            return texto
        print("Error: el campo no puede estar vacío. Intente nuevamente.")


def pedir_entero_positivo(mensaje):
    """Pide un entero mayor a cero (usado para población y superficie)."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("Error: debe ingresar un número entero válido.")
            continue
        if valor <= 0:
            print("Error: el valor debe ser mayor a cero.")
            continue
        return valor


def pedir_entero(mensaje):
    """Pide un entero sin restricción de signo (usado en rangos de filtros)."""
    while True:
        texto = input(mensaje).strip()
        try:
            return int(texto)
        except ValueError:
            print("Error: debe ingresar un número entero válido.")


# ============================================================
# ARCHIVOS lectura y escritura de CSV
# ============================================================

def cargar_paises(ruta):
    """
    Lee el CSV y devuelve una lista de diccionarios (uno por país).
    Si el archivo no existe o alguna línea está mal formada, informa el
    problema por consola y continúa (no interrumpe el programa).
    """
    paises = []

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"Aviso: no se encontró el archivo '{ruta}'. Se inicia con una lista vacía.")
        return paises

    if not lineas:
        return paises

    # La primera línea es el encabezado; los datos empiezan en la línea 2.
    for numero_linea, linea in enumerate(lineas[1:], start=2):
        linea = linea.strip()
        if not linea:
            continue

        campos = linea.split(",")
        if len(campos) != 4:
            print(f"Aviso: línea {numero_linea} del CSV mal formada, se ignora -> {linea}")
            continue

        nombre = campos[0]
        poblacion_texto = campos[1]
        superficie_texto = campos[2]
        continente = campos[3]

        try:
            poblacion = int(poblacion_texto)
            superficie = int(superficie_texto)
        except ValueError:
            print(f"Aviso: línea {numero_linea} tiene población o superficie no numérica, se ignora.")
            continue

        pais = {
            "nombre": nombre.strip(),
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente.strip(),
        }
        paises.append(pais)

    return paises


def guardar_paises(lista_paises, ruta):
    """Reescribe el CSV completo a partir de la lista actual de países."""
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(ENCABEZADO_CSV + "\n")
            for pais in lista_paises:
                campos = [
                    pais["nombre"],
                    str(pais["poblacion"]),
                    str(pais["superficie"]),
                    pais["continente"],
                ]
                archivo.write(",".join(campos) + "\n")
        return True
    except OSError as error:
        print(f"Error al guardar el archivo '{ruta}': {error}")
        return False


# ============================================================
# GESTIÓN (alta, actualización, búsqueda)
# ============================================================

def buscar_pais_exacto(lista_paises, nombre):
    """Busca por coincidencia exacta de nombre. Devuelve el diccionario o None."""
    for pais in lista_paises:
        if pais["nombre"].lower() == nombre.lower():
            return pais
    return None


def buscar_pais(lista_paises, texto):
    """Busca países cuyo nombre CONTENGA el texto (coincidencia parcial)."""
    texto = texto.lower().strip()
    resultado = []
    for pais in lista_paises:
        if texto in pais["nombre"].lower():
            resultado.append(pais)
    return resultado

def agregar_pais(lista_paises):
    """Pide los datos de un país nuevo y lo agrega, validando que no esté vacío ni duplicado."""
    print("\n--- Agregar nuevo país ---")
    nombre = pedir_texto_no_vacio("Nombre del país: ")

    if buscar_pais_exacto(lista_paises, nombre) is not None:
        print(f"Ya existe un país llamado '{nombre}'. No se agregó.")
        return

    poblacion = pedir_entero_positivo("Población: ")
    superficie = pedir_entero_positivo("Superficie en km²: ")
    continente = pedir_texto_no_vacio("Continente: ")

    lista_paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    })
    print(f"País '{nombre}' agregado correctamente.")


def actualizar_pais(lista_paises):
    """Busca un país por nombre exacto y actualiza su población y superficie."""
    print("\n--- Actualizar población y superficie ---")
    nombre = pedir_texto_no_vacio("Nombre del país a actualizar: ")
    pais = buscar_pais_exacto(lista_paises, nombre)

    if pais is None:
        print(f"No se encontró ningún país llamado '{nombre}'.")
        return

    print(f"  Datos actuales -> población: {pais['poblacion']}, superficie: {pais['superficie']} km²")
    pais["poblacion"] = pedir_entero_positivo("Nueva población: ")
    pais["superficie"] = pedir_entero_positivo("Nueva superficie en km²: ")
    print(f"País '{pais['nombre']}' actualizado correctamente.")


# ============================================================
# FILTROS
# ============================================================

def filtrar_por_continente(lista_paises, continente):
    continente = continente.lower().strip()
    resultado = []
    for pais in lista_paises:
        if pais["continente"].lower() == continente:
            resultado.append(pais)
    return resultado


def filtrar_por_poblacion(lista_paises, minimo, maximo):
    resultado = []
    for pais in lista_paises:
        if minimo <= pais["poblacion"] <= maximo:
            resultado.append(pais)
    return resultado


def filtrar_por_superficie(lista_paises, minimo, maximo):
    resultado = []
    for pais in lista_paises:
        if minimo <= pais["superficie"] <= maximo:
            resultado.append(pais)
    return resultado


# ============================================================
# FUNCIONES AUXILIARES PARA sorted() / max() / min()
# ============================================================

def obtener_nombre_minuscula(pais):
    """Devuelve el nombre del país en minúsculas, para ordenar alfabéticamente."""
    return pais["nombre"].lower()


def obtener_poblacion(pais):
    """Devuelve la población del país."""
    return pais["poblacion"]


def obtener_superficie(pais):
    """Devuelve la superficie del país."""
    return pais["superficie"]


# ============================================================
# ORDENAMIENTOS
# ============================================================

def ordenar_por_nombre(lista_paises, descendente=False):
    return sorted(lista_paises, key=obtener_nombre_minuscula, reverse=descendente)


def ordenar_por_poblacion(lista_paises, descendente=False):
    return sorted(lista_paises, key=obtener_poblacion, reverse=descendente)


def ordenar_por_superficie(lista_paises, descendente=False):
    return sorted(lista_paises, key=obtener_superficie, reverse=descendente)


# ============================================================
# ESTADÍSTICAS
# ============================================================

def pais_mayor_poblacion(lista_paises):
    if not lista_paises:
        return None
    return max(lista_paises, key=obtener_poblacion)


def pais_menor_poblacion(lista_paises):
    if not lista_paises:
        return None
    return min(lista_paises, key=obtener_poblacion)


def promedio_poblacion(lista_paises):
    if not lista_paises:
        return 0
    return sum(pais["poblacion"] for pais in lista_paises) / len(lista_paises)


def promedio_superficie(lista_paises):
    if not lista_paises:
        return 0
    return sum(pais["superficie"] for pais in lista_paises) / len(lista_paises)


def cantidad_por_continente(lista_paises):
    """Devuelve {continente: cantidad}."""
    conteo = {}
    for pais in lista_paises:
        continente = pais["continente"]
        conteo[continente] = conteo.get(continente, 0) + 1
    return conteo


# ============================================================
# PRESENTACIÓN (formateo de salida por consola)
# ============================================================

def mostrar_paises(lista_paises):
    """Muestra una lista de países."""
    if not lista_paises:
        print("(No hay países para mostrar)")
        return

    print("Nombre | Población | Superficie (km2) | Continente")
    print("-" * 60)
    for pais in lista_paises:
        print(f"{pais['nombre']} | {pais['poblacion']} | {pais['superficie']} | {pais['continente']}")


# ============================================================
# MENÚ Y CONTROL PRINCIPAL (con match/case)
# ============================================================

def mostrar_menu():
    print("\n========== GESTIÓN DE PAÍSES ==========")
    print("1. Agregar país")
    print("2. Actualizar población y superficie")
    print("3. Buscar país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("0. Salir")
    print("=========================================")


def menu_filtrar(lista_paises):
    print("\n--- Filtrar países ---")
    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    opcion = input("Seleccione una opción: ").strip()

    match opcion:
        case "1":
            continente = pedir_texto_no_vacio("Continente: ")
            resultado = filtrar_por_continente(lista_paises, continente)
        case "2":
            minimo = pedir_entero("Población mínima: ")
            maximo = pedir_entero("Población máxima: ")
            resultado = filtrar_por_poblacion(lista_paises, minimo, maximo)
        case "3":
            minimo = pedir_entero("Superficie mínima (km²): ")
            maximo = pedir_entero("Superficie máxima (km²): ")
            resultado = filtrar_por_superficie(lista_paises, minimo, maximo)
        case _:
            print("  -> Opción inválida.")
            return

    print(f"\nSe encontraron {len(resultado)} país/es:")
    mostrar_paises(resultado)


def menu_ordenar(lista_paises):
    print("\n--- Ordenar países ---")
    print("1. Por nombre")
    print("2. Por población")
    print("3. Por superficie")
    opcion = input("Seleccione una opción: ").strip()

    if opcion not in ("1", "2", "3"):
        print("  -> Opción inválida.")
        return

    orden = input("¿Ascendente o descendente? (A/D): ").strip().lower()

    if orden == "d":
        descendente = True
    else:
        descendente = False

    match opcion:
        case "1":
            resultado = ordenar_por_nombre(lista_paises, descendente)
        case "2":
            resultado = ordenar_por_poblacion(lista_paises, descendente)
        case "3":
            resultado = ordenar_por_superficie(lista_paises, descendente)

    mostrar_paises(resultado)


def menu_estadisticas(lista_paises):
    print("\n--- Estadísticas ---")
    if not lista_paises:
        print("  (No hay países cargados)")
        return

    mayor = pais_mayor_poblacion(lista_paises)
    menor = pais_menor_poblacion(lista_paises)
    print(f"País con mayor población: {mayor['nombre']} ({mayor['poblacion']:,})")
    print(f"País con menor población: {menor['nombre']} ({menor['poblacion']:,})")
    print(f"Promedio de población:    {promedio_poblacion(lista_paises):,.2f}")
    print(f"Promedio de superficie:   {promedio_superficie(lista_paises):,.2f} km²")

    print("  Cantidad de países por continente:")
    for continente, cantidad in cantidad_por_continente(lista_paises).items():
        print(f"- {continente}: {cantidad}")


def main():
    lista_paises = cargar_paises(RUTA_CSV)
    print(f"Se cargaron {len(lista_paises)} país/es desde '{RUTA_CSV}'.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                agregar_pais(lista_paises)
                guardar_paises(lista_paises, RUTA_CSV)
            case "2":
                actualizar_pais(lista_paises)
                guardar_paises(lista_paises, RUTA_CSV)
            case "3":
                texto = pedir_texto_no_vacio("Nombre (o parte del nombre) a buscar: ")
                resultados = buscar_pais(lista_paises, texto)
                print(f"\nSe encontraron {len(resultados)} país/es:")
                mostrar_paises(resultados)
            case "4":
                menu_filtrar(lista_paises)
            case "5":
                menu_ordenar(lista_paises)
            case "6":
                menu_estadisticas(lista_paises)
            case "0":
                print("Hasta luego.")
                break
            case _:
                print("Opción inválida, intente nuevamente.")


if __name__ == "__main__":
    main()