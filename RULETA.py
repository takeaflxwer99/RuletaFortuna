import random
import time

### VARIABLES PRINCIPALES
jugadores = ['jugador1', 'jugador2', 'jugador3']

# Creamos un diccionario que guarde el dinero/puntuacion de cada jugador
puntuaciones = {
    'jugador1': 0,
    'jugador2': 0,
    'jugador3': 0
    }

# Creamos otro diccionario que guarde las letras acertadas
letras_acertadas = {}

# Escribimos aparte en un documento de tipo '.txt' las frases y pistas que hemos elegido
fichero_frases = "panel_pistas.txt"

# Cremos una lista que guarde los paneles que ya han salido para no repetirlos
paneles_jugados = []

turno_actual = 0

#-----------------------------------------------------------------------------------------

### FUNCIONES RELACIONADAS CON EL PANEL

# Seleccionamos aleatoriamente una frase y su pista desde el archivo
def seleccionar_frase(fichero):
    # Abrimos el archivo en el que hemos guardado las frases y pistas
    with open(fichero, 'r', encoding='utf-8') as fich:
        # Leemos todas las lineas del archivo
        lineas = fich.readlines()

    # Elegimos las lineas que contengan el símbolo '|'
    lineas_validas = [l for l in lineas if '|' in l]

    # Seleccionamos las frases que todavia no se han jugado
    disponibles = [l for l in lineas_validas if l.strip().split('|')[0].upper() not in paneles_jugados]

    # Si no hay frases disponibles, se han jugado todas y el juego termina
    if not disponibles:
        print("\n¡Se han jugado todos los paneles! Fin del juego.")
        exit()

    # De las lineas validas, se elige aleatoriamente una frase y su pista correspondiente
    frase, pista = random.choice(disponibles).strip().split('|')
    
    # La frase seleccionada se añade a la lista de los paneles ya jugados
    paneles_jugados.append(frase.upper())
    
    # Devolvemos la frase y su pista
    return frase.upper(), pista


# Mostramos el panel con las letras acertadas hasta el momento
def mostrar_panel(frase, letras_acertadas, pista):
    # Mostramos una letra si ha sido acertada
    # Si no ha sido acertada, mostramos un espacio "_"
    panel_mostrado = [letra if letra in letras_acertadas or letra == ' ' else '_' for letra in frase]
    
    # Mostramos la pista y el panel actual
    print("\n" + "="*40)
    print(f"📌  PISTA: {pista}")
    print("\n>   PANEL:")
    print("\n   " + " ".join(panel_mostrado))
    print("\n" + "="*40)

#-----------------------------------------------------------------------------------------

### FUNCIONES RELACIONADAS CON EL JUEGO

# Elegimos aleatoriamente al jugador que empieza
def elegir_jugador():
    print('\nEligiendo jugador...')
    turno = random.randint(0, len(jugadores) - 1)  # Se escoge un jugador aleatorio
    time.sleep(2) # Simula una pausa
    return turno


# Simulamos el giro de la ruleta y devolvemos el resultado
# El resultado puede ser dinero o una casilla especial
def girar_ruleta():
    opciones = ['0', '25', '50', '75', '100', '150', 'Pierde turno', 'Quiebra', 'Me lo quedo', 'Se lo doy']
    resultado = random.choice(opciones)  # Se escoge una opcion de la ruleta de manera aleatoria
    time.sleep(2) # Simula una pausa
    return resultado


# Verificamos si la letra esta en la frase
def comprobar_letra(letra, frase, letras_acertadas):
    letra = letra.upper()  # Todas las letras se ponen en mayuscula
    if letra in letras_acertadas:
        print("Esa letra ya se ha dicho. Intenta con otra distinta.")
        return False
    if letra in frase:
        # Añadimos las letras acertadas al diccionario que las guarda
        letras_acertadas[letra] = letras_acertadas.get(letra, 0) + 1
        return True
    return False


# Comprobamos si la frase que se ha introducido es correcta
def comprobar_frase(frase_correcta, frase_usuario):
    return frase_correcta.strip().upper() == frase_usuario.strip().upper()


# Sumamos o restamos puntos segun el resultado de la ruleta
def sumar_puntos(jugador, resultado, otrojugador):
    if resultado.isdigit():
        # Convertimos el resultado a entero
        puntos = int(resultado)
        # Sumamos los puntos al jugador actual
        puntuaciones[jugador] += puntos
        print(f"\n{jugador} ha sumado {puntos} puntos.")
        
    elif resultado == "Quiebra":
        # Si cae en Quiebra, el jugador pierde todos sus puntos
        puntuaciones[jugador] = 0 
        print(f"\n{jugador} ha perdido todo su dinero.")
        
    elif resultado == "Me lo quedo":
        # El jugador roba los puntos de otro jugador de su eleccion
        puntuaciones[jugador] += puntuaciones[otrojugador]
        puntuaciones[otrojugador] = 0
        print(f"\n{jugador} ha robado los puntos de {otrojugador}.")
        
    elif resultado == "Se lo doy":
        # El jugador da sus puntos a otro jugador de su eleccion
        puntuaciones[otrojugador] += puntuaciones[jugador]
        puntuaciones[jugador] = 0
        print(f"\n{jugador} ha dado sus puntos a {otrojugador}.")

# Comprobamos que tipo de casilla (dinero o especial) ha salido y que hacer
def comprobar_gajo(jugador, resultado, frase, pista):
    global turno_actual

    if resultado == 'Me lo quedo':
        letra = input('\n¿Qué letra quieres? ').upper()
        if comprobar_letra(letra, frase, letras_acertadas):
            mostrar_panel(frase, letras_acertadas, pista)
            while True:
                otrojugador_input = input('\n¿A qué jugador quieres robarle los puntos? ')
                otrojugador = otrojugador_input.lower().replace(" ", "")
                if otrojugador not in jugadores:
                    print("Entrada no válida. Solo puedes elegir: jugador 1, jugador 2 o jugador 3.")
                elif otrojugador == jugador:
                    print("No puedes seleccionar tu propio nombre. Elige a otro jugador.")
                else:
                    break
            sumar_puntos(jugador, resultado, otrojugador)
            while True:
                resolver = input('\n¿Quieres resolver el panel? (sí/no): ').strip().lower()
                if resolver in ['si', 'sí', 'no']:
                    break
                else:
                    print("Por favor, responde con 'sí' o 'no'.")
            if resolver in ['si', 'sí']:
                posible_solucion = input('\nEscribe aquí tu solución: ')
                if comprobar_frase(frase, posible_solucion):
                    print('\n¡Has resuelto el panel correctamente! Enhorabuena :)')
                    return False, False
                else:
                    print('\nNo era esa la respuesta... ¡pierdes el turno!')
                    turno_actual = (turno_actual + 1) % len(jugadores)
                    return True, True
            else:
                return True, False
        else:
            turno_actual = (turno_actual + 1) % len(jugadores)
            return True, True

    elif resultado == 'Se lo doy':
        print(f"\n{jugador} tiene que darle los puntos a otro jugador y pierde su turno.")
        while True:
            otrojugador_input = input('\n¿A qué jugador quieres darle tus puntos? ')
            otrojugador = otrojugador_input.lower().replace(" ", "")
            if otrojugador not in jugadores:
                print("Entrada no válida. Solo puedes elegir: jugador 1, jugador 2 o jugador 3.")
            elif otrojugador == jugador:
                print("No puedes seleccionar tu propio nombre. Elige a otro jugador.")
            else:
                break
        sumar_puntos(jugador, resultado, otrojugador)
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True, True

    elif resultado == 'Pierde turno':
        print(f"\n{jugador} pierde su turno.")
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True, True

    elif resultado == 'Quiebra':
        sumar_puntos(jugador, resultado, '')
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True, True

    else:
        letra = input('\n¿Qué letra quieres? ').upper()
        if comprobar_letra(letra, frase, letras_acertadas):
            mostrar_panel(frase, letras_acertadas, pista)
            sumar_puntos(jugador, resultado, '')
            while True:
                resolver = input('\n¿Quieres resolver el panel? (sí/no): ').strip().lower()
                if resolver in ['si', 'sí', 'no']:
                    break
                else:
                    print("Por favor, responde con 'sí' o 'no'.")
            if resolver in ['si', 'sí']:
                posible_solucion = input('\nEscribe aquí tu solución: ')
                if comprobar_frase(frase, posible_solucion):
                    print('\n¡Has resuelto el panel correctamente! Enhorabuena :)')
                    return False, False
                else:
                    print('\nNo era esa la respuesta... ¡pierdes el turno!')
                    turno_actual = (turno_actual + 1) % len(jugadores)
                    return True, True
            else:
                return True, False
        else:
            turno_actual = (turno_actual + 1) % len(jugadores)
            return True, True

#-----------------------------------------------------------------------------------------

### FUNCION PARA MOSTRAR AL GANADOR

# El jugador que más puntos tenga al final gana
def ganador():
    puntos_max = max(puntuaciones.values())
    jugador_ganador = []
    for jugador, puntos in puntuaciones.items():
        if puntos == puntos_max:
            jugador_ganador.append(jugador)
    if len(jugador_ganador) == 1:
        print(f"\n¡¡¡Ha ganado el {jugador_ganador[0]} con {puntos_max} puntos!!!")
    else:
        print(f"\nHay empate entre {', y '.join(jugador_ganador)} con {puntos_max} puntos cada uno")

#-----------------------------------------------------------------------------------------

### FUNCIÓN PRINCIPAL

# Esta funcion principal combina el resto de funciones
# Crea el juego en si
def juego_ruleta():
    global turno_actual
    while True:
        letras_acertadas.clear()
        panel_original, pista = seleccionar_frase(fichero_frases)
        turno_actual = elegir_jugador()
        solucion = True

        print(f"\n>>> Turno de {jugadores[turno_actual]} <<<")
        mostrar_panel(panel_original, letras_acertadas, pista)

        while solucion:
            input('\nPulsa ENTER para girar la ruleta...')
            resultado = girar_ruleta()
            print(f"\nHas caído en: {resultado}")

            jugador = jugadores[turno_actual]
            solucion, cambio_turno = comprobar_gajo(jugador, resultado, panel_original, pista)

            if cambio_turno:
                print("\nPuntuaciones actuales:")
                for j in puntuaciones:
                    print(f"{j}: {puntuaciones[j]}")
                print("\n--- Siguiente turno ---")
                print(f"\n>>> Turno de {jugadores[turno_actual]} <<<")
                mostrar_panel(panel_original, letras_acertadas, pista)

        otra_partida = input("\n¿Quieres jugar otra partida? (sí/no): ").strip().lower()
        if otra_partida not in ['si', 'sí']:
            print("\n¡Gracias por jugar!")
            ganador()
            break

#-----------------------------------------------------------------------------------------

### EJECUTAR JUEGO

if __name__ == "__main__":
    juego_ruleta()
