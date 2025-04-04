import random
import time
#DEFINICION DE VARIABLES
# --- VARIABLES GLOBALES ---
jugadores = ['jugador1', 'jugador2', 'jugador3']

# Creamos un diccionario para guardar la puntuación de cada jugador
puntuaciones = {
    'jugador1': 0,
    'jugador2': 0,
    'jugador3': 0
}
#hola aqui mi comentario molon

# Diccionario para guardar letras acertadas por los jugadores
letras_acertadas = {}

# Ruta del fichero con frases y pistas
fichero_frases = "panel_pistas.txt"


# --- FUNCIONES DEL PANEL ---

# Seleccionamos aleatoriamente una frase y su pista desde el archivo
def seleccionar_frase(fichero):
    with open(fichero, 'r', encoding='utf-8') as fich:
        # Leemos todas las líneas del archivo
        lineas = fich.readlines()

    # Filtramos las líneas que contienen el símbolo '|'
    lineas_validas = [l for l in lineas if '|' in l]

    # Verificamos si hay líneas válidas
    if not lineas_validas:
        raise ValueError("El archivo no contiene frases válidas con formato 'frase|pista'.")

    # Elegimos aleatoriamente una línea válida
    frase, pista = random.choice(lineas_validas).strip().split('|')
    return frase.upper(), pista


# Mostramos el panel con las letras acertadas hasta el momento
def mostrar_panel(frase, letras_acertadas, pista):
    # Mostramos una letra si ha sido acertada o es un espacio; si no, mostramos "_"
    panel_mostrado = [letra if letra in letras_acertadas or letra == ' ' else '_' for letra in frase]
    print("\nPista:", pista)
    print("Panel:", " ".join(panel_mostrado))


# --- FUNCIONES DE JUEGO ---

# Elegimos aleatoriamente al jugador que empieza
def elegir_jugador():
    print('Eligiendo jugador...')
    turno_actual = random.randint(0, len(jugadores) - 1)
    time.sleep(2)
    return turno_actual


# Simulamos el giro de la ruleta y devolvemos el resultado
def girar_ruleta():
    opciones = ['0', '25', '50', '75', '100', '150', 'Pierde turno', 'Quiebra', 'Me lo quedo', 'Se lo doy']
    resultado = random.choice(opciones)
    time.sleep(2)
    return resultado


# Verificamos si la letra está en la frase
def comprobar_letra(letra, frase, letras_acertadas):
    letra = letra.upper()
    if letra in frase:
        # Sumamos al diccionario de letras acertadas
        letras_acertadas[letra] = letras_acertadas.get(letra, 0) + 1
        return True
    return False


# Comprobamos si la frase que introdujo el jugador es correcta
def comprobar_frase(frase_correcta, frase_usuario):
    return frase_correcta.strip().upper() == frase_usuario.strip().upper()


# Sumamos o restamos puntos según el resultado de la ruleta
def sumar_puntos(jugador, resultado, otrojugador):
    if resultado.isdigit():
        # Convertimos el resultado a entero
        puntos = int(resultado)
        # Sumamos los puntos al jugador actual
        puntuaciones[jugador] += puntos
        print(f"{jugador} ha sumado {puntos} puntos.")
    elif resultado == "Quiebra":
        # Si cae en Quiebra, el jugador pierde todos sus puntos
        puntuaciones[jugador] = 0
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


# Comprobamos qué tipo de casilla ha salido y qué hacer
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
                    return True
            else:
                return True
        else:
            print('La letra no está en el panel.')
            turno_actual = (turno_actual + 1) % len(jugadores)
            return True

    elif resultado == 'Se lo doy':
        print(f"{jugadores[turno_actual]} tiene que darle los puntos a otro jugador y pierde su turno.")
        otrojugador = input('¿A qué jugador quieres darle tus puntos? ')
        sumar_puntos(jugador, resultado, otrojugador)
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True

    elif resultado == 'Pierde turno':
        print(f"{jugadores[turno_actual]} pierde su turno.")
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

    # Seleccionamos la frase del panel y la pista desde el archivo
    panel_original, pista = seleccionar_frase(fichero_frases)

    # Elegimos aleatoriamente quién empieza
    turno_actual = elegir_jugador()
    solucion = True

    print(f"\nTurno de {jugadores[turno_actual]}")
    mostrar_panel(panel_original, letras_acertadas, pista)

    # Bucle principal del juego
    while solucion:
        input('\nPulsa ENTER para girar la ruleta...')
        resultado = girar_ruleta()
        print('Has caído en:', resultado)

        jugador = jugadores[turno_actual]
        solucion = comprobar_gajo(jugador, resultado, panel_original, pista)

        # Mostramos las puntuaciones actualizadas
        print("\nPuntuaciones:")
        for j in puntuaciones:
            print(f"{j}: {puntuaciones[j]}")
        print("\n--- Siguiente turno ---")


# --- EJECUTAR JUEGO ---
juego_ruleta()
