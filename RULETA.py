import random
import time
## DEFINICION DE VARIABLES
letras_acertadas = {}
archivo_txt = "panel_pistas.txt"
jugadores = ['jugador1', 'jugador2', 'jugador3'] # creamos una lista con los jugadores
fichero_frases = "panel_pistas.txt"
paneles_jugados = []
# Utilizamos un diccionario que guarde el dinero de cada jugador
puntuaciones = {'jugador1': 0,
                'jugador2': 0,
                'jugador3': 0}

# Creamos otro diccionario para guardar las letras que acierten los jugadores
letras_acertadas = {}

# Archivo que contiene las frases y pistas
fichero_frases = "panel_pistas.txt"

#---------------------------------------------------------------------------------#
## FUNCIONES DEL PANEL 

# Funcion para seleccionar aleatoriamente la frase desde el archivo
def seleccionar_frase(fichero, paneles_jugados):
    with open(fichero, 'r', encoding='utf-8') as fich:
        lineas = fich.readlines()

    lineas_validas = [l for l in lineas if '|' in l]
    disponibles = [l for l in lineas_validas if l.strip().split('|')[0].upper() not in paneles_jugados]

    if not disponibles:
        print("¡Se han jugado todos los paneles! Fin del juego.")
        exit()

    frase, pista = random.choice(disponibles).strip().split('|')
    paneles_jugados.append(frase.upper())
    return frase.upper(), pista

def mostrar_panel(frase, letras_acertadas, pista):
    panel_mostrado = [letra if letra in letras_acertadas or letra == ' ' else '_' for letra in frase]
    print("\nPista:", pista)
    print("Panel:", " ".join(panel_mostrado))


## FUNCIONES DEL JUEGO Y LAS NORMAS

# Funcion que elige que jugador empieza el juego
def elegir_jugador():
    print('Eligiendo jugador...')
    turno_actual = random.randint(0, len(jugadores) - 1) # eleccion aleatoria de un jugador de la lista
    time.sleep(2) # usamos time.sleep para simular el giro con una pausa
    return turno_actual


# Funcion que gira la ruleta en el turno inicial
def girar_ruleta():
    opciones = ['0','25','50','75','100','150','Pierde turno','Quiebra', 'Me lo quedo', 'Se lo doy']
    resultado = random.choice(opciones)
    time.sleep(2)
    return resultado


# Comprobamos si la letra está en la frase
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


# Funcion que comprueba si el gajo es puntuacion (dinero) o casillas especiales
def comprobar_gajo(jugador, resultado, frase, pista):
    global turno_actual
    # ME LO QUEDO: a quien le toque robará dinero a otro jugador y dirá una letra
    # si acierta la letra se queda con el dinero
    # si falla la letra no se lo queda
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
        
    # SE LO DOY: a quien le toque tiene que darle el dinero al jugador que elija
    # además pierde el turno
    elif resultado == 'Se lo doy':
        print(f"{jugadores[turno_actual]} tiene que darle los puntos a otro jugador y pierde su turno.")
        otrojugador = input('¿A qué jugador quieres darle tus puntos? ')
        sumar_puntos(jugador, resultado, otrojugador)
        turno_actual = (turno_actual + 1) % len(jugadores)
        print(f"Ahora le toca a {jugadores[turno_actual]}")
        return True
    
    # PIERDE TURNO: a quien le toque perderá su turno
    # no pierde el dinero
    elif resultado == 'Pierde turno':
        print(f"{jugadores[turno_actual]} pierde su turno.")
        turno_actual = (turno_actual + 1) % len(jugadores)
        print(f"Ahora le toca a {jugadores[turno_actual]}")
        return True
    
    # QUIEBRA: a quien le toque perderá todo el dinero
    # además también pierde el turno
    elif resultado == 'Quiebra':
        sumar_puntos(jugador, resultado, '')
        turno_actual = (turno_actual + 1) % len(jugadores)
        print(f"Ahora le toca a {jugadores[turno_actual]}")
        return True
    
    # DINERO: gajos que no son especiales, la puntuación
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

#---------------------------------------------------------------------------------#
# FUNCIÓN PRINCIPAL
def juego_ruleta():
    global turno_actual
    while True: #con esto se reiniciara el juego cada vez que un panel se resuelva
        # Seleccionamos la frase del panel y la pista desde el archivo
        
        panel_original, pista = seleccionar_frase(fichero_frases, paneles_jugados)
        letras_acertadas.clear() #reiniciamos las letras acertadas cuando empezamos un nuevo panel
        # Elegimos aleatoriamente quién empieza
        turno_actual = elegir_jugador()
        solucion = True


    # Se elige aleatoriamente una frase del panel guardada en el archivo panel_pistas.txt
    panel_original, pista = seleccionar_frase(fichero_frases, paneles_jugados)

    # Llamamos a elegir_jugador para seleccionar un jugador aleatoriamente
    turno_actual = elegir_jugador()
    solucion = True

    print(f"\nTurno de {jugadores[turno_actual]}")
    mostrar_panel(panel_original, letras_acertadas, pista)

    # Bucle principal del juego
    while solucion:
        input('\nPulsa ENTER para girar la ruleta...')
        # Llamamos a girar_ruleta
        resultado = girar_ruleta()
        print('Has caído en:', resultado)

        jugador = jugadores[turno_actual]
        # Llamamos a comprobar_gajo
        solucion = comprobar_gajo(jugador, resultado, panel_original, pista)

        # Mostramos las puntuaciones actualizadas
        print("\nPuntuaciones:")
        for j in puntuaciones:
            print(f"{j}: {puntuaciones[j]}")
        print("\n--- Siguiente turno ---")

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
            print(f"\nTurno de {jugadores[turno_actual]}")
            print("\n--- Siguiente turno ---")
            
        otra_partida = input("¿Quieres jugar otra partida? (si/no): ").strip().lower()
        if otra_partida != 'si':
            print("¡Gracias por jugar!")
            break  # Salir del bucle y terminar el juego

# Llamamos a juego_ruleta, la funcion principal para ejecutar todo el programa
juego_ruleta()
