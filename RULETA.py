import random
import time

# --- VARIABLES GLOBALES ---
jugadores = ['jugador1', 'jugador2', 'jugador3']

# Creamos un diccionario para guardar la puntuación de cada jugador
puntuaciones = {
    'jugador1': 0,
    'jugador2': 0,
    'jugador3': 0
}

# Diccionario para guardar letras acertadas por los jugadores
letras_acertadas = {}

# Ruta del fichero con frases y pistas
fichero_frases = "panel_pistas.txt"
# Lista para almacenar las frases ya jugadas
paneles_jugados = []  # Frases que ya han sido utilizadas
turno_actual = 0


# --- FUNCIONES DEL PANEL ---

# Función para seleccionar aleatoriamente una frase y su pista desde el archivo
def seleccionar_frase(fichero):
    # Abrimos el archivo con las frases y pistas
    with open(fichero, 'r', encoding='utf-8') as fich:
        # Leemos todas las líneas del archivo
        lineas = fich.readlines()

    # Filtramos las líneas que contienen el símbolo '|'
    lineas_validas = [l for l in lineas if '|' in l]

    # Filtramos las frases que no se han jugado ya
    disponibles = [l for l in lineas_validas if l.strip().split('|')[0].upper() not in paneles_jugados]

    # Si no hay frases disponibles, terminamos el juego
    if not disponibles:
        print("¡Se han jugado todos los paneles! Fin del juego.")
        exit()

    # Elegimos aleatoriamente una línea válida (frase y pista)
    frase, pista = random.choice(disponibles).strip().split('|')
    
    # Añadimos la frase seleccionada a la lista de paneles jugados
    paneles_jugados.append(frase.upper())
    
    # Devolvemos la frase y su pista
    return frase.upper(), pista


# Función para mostrar el panel con las letras acertadas hasta el momento
def mostrar_panel(frase, letras_acertadas, pista):
    # Creamos una lista donde mostramos una letra si ha sido acertada o si es un espacio, 
    # y un "_" si no ha sido acertada
    panel_mostrado = [letra if letra in letras_acertadas or letra == ' ' else '_' for letra in frase]
    
    # Mostramos la pista y el panel actual
    print("\nPista:", pista)
    print("Panel:", " ".join(panel_mostrado))


# --- FUNCIONES DE JUEGO ---

# Función para elegir aleatoriamente al jugador que empieza
def elegir_jugador():
    print('Eligiendo jugador...')
    turno = random.randint(0, len(jugadores) - 1)  # Elegimos un jugador aleatorio
    time.sleep(2)
    return turno


# Función para simular el giro de la ruleta
def girar_ruleta():
    opciones = ['0', '25', '50', '75', '100', '150', 'Pierde turno', 'Quiebra', 'Me lo quedo', 'Se lo doy']
    resultado = random.choice(opciones)  # Elegimos un resultado aleatorio de la ruleta
    time.sleep(2)
    return resultado


# Función para comprobar si una letra está en la frase
def comprobar_letra(letra, frase, letras_acertadas):
    letra = letra.upper()  # Aseguramos que la letra esté en mayúsculas
    if letra in frase:
        # Sumamos al diccionario de letras acertadas
        letras_acertadas[letra] = letras_acertadas.get(letra, 0) + 1
        return True
    return False


# Función para comprobar si la frase introducida por el jugador es correcta
def comprobar_frase(frase_correcta, frase_usuario):
    return frase_correcta.strip().upper() == frase_usuario.strip().upper()


# Función para sumar o restar puntos según el resultado de la ruleta
def sumar_puntos(jugador, resultado, otrojugador):
    if resultado.isdigit():
        # Convertimos el resultado a entero si es un número
        puntos = int(resultado)
        puntuaciones[jugador] += puntos  # Sumamos los puntos al jugador actual
        print(f"{jugador} ha sumado {puntos} puntos.")
    elif resultado == "Quiebra":
        puntuaciones[jugador] = 0  # El jugador pierde todos sus puntos
        print(f"{jugador} ha perdido todo su dinero.")
    elif resultado == "Me lo quedo":
        # El jugador roba los puntos del otro jugador
        puntuaciones[jugador] += puntuaciones[otrojugador]
        puntuaciones[otrojugador] = 0
        print(f"{jugador} ha robado los puntos de {otrojugador}.")
    elif resultado == "Se lo doy":
        # El jugador da sus puntos al otro jugador
        puntuaciones[otrojugador] += puntuaciones[jugador]
        puntuaciones[jugador] = 0
        print(f"{jugador} ha dado sus puntos a {otrojugador}.")


# Función para comprobar qué tipo de casilla ha salido en la ruleta y cómo actuar
def comprobar_gajo(jugador, resultado, frase, pista):
    global turno_actual
    if resultado == 'Me lo quedo':
        letra = input('¿Qué letra quieres? ').upper()
        if comprobar_letra(letra, frase, letras_acertadas):
            mostrar_panel(frase, letras_acertadas, pista)
            otrojugador = input('¿A qué jugador quieres robarle los puntos? ')
            sumar_puntos(jugador, resultado, otrojugador)
            resolver = input('¿Quieres resolver el panel? (si/no) ').lower()
            if resolver == 'si':
                posible_solucion = input('Escribe aquí tu solución: ')
                if comprobar_frase(frase, posible_solucion):
                    print('¡Has resuelto el panel correctamente! Enhorabuena :)')
                    return False
                else:
                    print('No era esa la respuesta... ¡pierdes el turno!')
                    turno_actual = (turno_actual + 1) % len(jugadores)
                    print(f"Ahora le toca a {jugadores[turno_actual]}")
                    return True
            else:
                return True
        else:
            print('La letra no está en el panel.')
            turno_actual = (turno_actual + 1) % len(jugadores)
            print(f"Ahora le toca a {jugadores[turno_actual]}")
            return True

    elif resultado == 'Se lo doy':
        print(f"{jugador} tiene que darle los puntos a otro jugador y pierde su turno.")
        otrojugador = input('¿A qué jugador quieres darle tus puntos? ')
        sumar_puntos(jugador, resultado, otrojugador)
        turno_actual = (turno_actual + 1) % len(jugadores)
        print(f"Ahora le toca a {jugadores[turno_actual]}")
        return True

    elif resultado == 'Pierde turno':
        print(f"{jugador} pierde su turno.")
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True

    elif resultado == 'Quiebra':
        sumar_puntos(jugador, resultado, '')
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True

    else:
        letra = input('¿Qué letra quieres? ').upper()
        if comprobar_letra(letra, frase, letras_acertadas):
            mostrar_panel(frase, letras_acertadas, pista)
            sumar_puntos(jugador, resultado, '')
            resolver = input('¿Quieres resolver el panel? (si/no) ').lower()
            if resolver == 'si':
                posible_solucion = input('Escribe aquí tu solución: ')
                if comprobar_frase(frase, posible_solucion):
                    print('¡Has resuelto el panel correctamente! Enhorabuena :)')
                    return False
                else:
                    print('No era esa la respuesta... ¡pierdes el turno!')
                    turno_actual = (turno_actual + 1) % len(jugadores)
                    return True
            else:
                return True
        else:
            print('La letra no está en el panel.')
            turno_actual = (turno_actual + 1) % len(jugadores)
            return True


# --- FUNCIÓN PRINCIPAL ---

def juego_ruleta():
    global turno_actual
    while True:
        letras_acertadas.clear()  # Limpiamos las letras acertadas al empezar cada partida
        panel_original, pista = seleccionar_frase(fichero_frases)  # Seleccionamos la frase y pista
        turno_actual = elegir_jugador()  # Elegimos el primer jugador
        solucion = True

        print(f"\nTurno de {jugadores[turno_actual]}")
        mostrar_panel(panel_original, letras_acertadas, pista)  # Mostramos el panel inicial

        while solucion:
            input('\nPulsa ENTER para girar la ruleta...')
            resultado = girar_ruleta()  # Giramos la ruleta
            print('Has caído en:', resultado)

            jugador = jugadores[turno_actual]
            solucion = comprobar_gajo(jugador, resultado, panel_original, pista)  # Comprobamos la ruleta

            print("\nPuntuaciones:")
            for j in puntuaciones:
                print(f"{j}: {puntuaciones[j]}")
            print("\n--- Siguiente turno ---")

            if solucion:
                print(f"\nTurno de {jugadores[turno_actual]}")
                mostrar_panel(panel_original, letras_acertadas, pista)

        otra_partida = input("¿Quieres jugar otra partida? (si/no): ").strip().lower()
        if otra_partida != 'si':
            print("¡Gracias por jugar!")
            break  # Si no quiere jugar otra, salimos del bucle


# --- EJECUTAR JUEGO ---
if __name__ == "__main__":
    RULETA()