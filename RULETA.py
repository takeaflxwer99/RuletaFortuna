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
        print("¡Se han jugado todos los paneles! Fin del juego.")
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
    print("\nPista:", pista)
    print("Panel:", " ".join(panel_mostrado))

#-----------------------------------------------------------------------------------------

### FUNCIONES RELACIONADAS CON EL JUEGO

# Elegimos aleatoriamente al jugador que empieza
def elegir_jugador():
    print('Eligiendo jugador...')
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
        print(f"{jugador} ha sumado {puntos} puntos.")
        
    elif resultado == "Quiebra":
        # Si cae en Quiebra, el jugador pierde todos sus puntos
        puntuaciones[jugador] = 0 
        print(f"{jugador} ha perdido todo su dinero.")
        
    elif resultado == "Me lo quedo":
        # El jugador roba los puntos de otro jugador de su eleccion
        puntuaciones[jugador] += puntuaciones[otrojugador]
        puntuaciones[otrojugador] = 0
        print(f"{jugador} ha robado los puntos de {otrojugador}.")
        
    elif resultado == "Se lo doy":
        # El jugador da sus puntos a otro jugador de su eleccion
        puntuaciones[otrojugador] += puntuaciones[jugador]
        puntuaciones[jugador] = 0
        print(f"{jugador} ha dado sus puntos a {otrojugador}.")


# Comprobamos que tipo de casilla (dinero o especial) ha salido y que hacer
def comprobar_gajo(jugador, resultado, frase, pista):
    global turno_actual
    # ME LO QUEDO: el jugador roba los puntos de otro jugador que el elija
    # primero dira una letra, si la acierta se queda con el dinero
    # si la falla, no puede robar nada
    if resultado == 'Me lo quedo':
        letra = input('¿Qué letra quieres? ').upper() # Ponemos la letra en mayusculas
        if comprobar_letra(letra, frase, letras_acertadas):
            mostrar_panel(frase, letras_acertadas, pista)
            otrojugador = input('¿A qué jugador quieres robarle los puntos? ')
            sumar_puntos(jugador, resultado, otrojugador)
            resolver = input('¿Quieres resolver el panel? (si/no) ').lower() # Ponemos la palabra en minuscula
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
    
    # SE LO DOY: el jugador escogera otro jugador para darle sus puntos
    elif resultado == 'Se lo doy':
        print(f"{jugador} tiene que darle los puntos a otro jugador y pierde su turno.")
        otrojugador = input('¿A qué jugador quieres darle tus puntos? ')
        sumar_puntos(jugador, resultado, otrojugador)
        turno_actual = (turno_actual + 1) % len(jugadores)
        print(f"Ahora le toca a {jugadores[turno_actual]}")
        return True
    
    # PIERDE TURNO: el jugador pierde su turno
    # no pierde el dinero
    elif resultado == 'Pierde turno':
        print(f"{jugador} pierde su turno.")
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True
    
    # QUIEBRA: el jugador pierde todos sus puntos
    # ademas tambien pierde el turno
    elif resultado == 'Quiebra':
        sumar_puntos(jugador, resultado, '')
        turno_actual = (turno_actual + 1) % len(jugadores)
        return True
    
    # PUNTUACION: el jugador gana dinero/puntos
    else:
        letra = input('¿Qué letra quieres? ').upper() # Ponemos la letra en mayusculas
        if comprobar_letra(letra, frase, letras_acertadas):
            mostrar_panel(frase, letras_acertadas, pista)
            sumar_puntos(jugador, resultado, '')
            resolver = input('¿Quieres resolver el panel? (si/no) ').lower() # Ponemos la palabra en minuscula
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

#-----------------------------------------------------------------------------------------

### FUNCION PARA MOSTRAR AL GANADOR

# El jugador que más puntos tenga al final gana
def ganador():
    # Entre las puntuaciones de los 3 jugadores, busca la más alta
    puntos_max = max(puntuaciones.values())
    
    jugador_ganador = []  # lista que guarda al ganador
    
    for jugador, puntos in puntuaciones.items():
        # El jugador que tenga la puntuacion más alta se añade a la lista
        if puntos == puntos_max:
            jugador_ganador.append(jugador)
            
    # Si no hay empate
    if len(jugador_ganador) == 1:
        print(f"\n¡¡¡Ha ganado el {jugador_ganador[0]} con {puntos_max} puntos!!!")
    # Si hay empate
    else:
        print(f"\nHay empate entre {', y '.join(jugador_ganador)} con {puntos_max} puntos cada uno")

#-----------------------------------------------------------------------------------------

### FUNCIÓN PRINCIPAL

# Esta funcion principal combina el resto de funciones
# Crea el juego en si
def juego_ruleta():
    global turno_actual
    while True:
        letras_acertadas.clear()  # Limpiamos el diccionario de las letras acertadas al empezar cada partida
        panel_original, pista = seleccionar_frase(fichero_frases)  # Seleccionamos aleatoriamente la frase y pista
        turno_actual = elegir_jugador()  # Elegimos el primer jugador al azar
        solucion = True

        print(f"\nTurno de {jugadores[turno_actual]}")
        mostrar_panel(panel_original, letras_acertadas, pista)  # Mostramos el panel inicial

        while solucion:
            input('\nPulsa ENTER para girar la ruleta...')
            resultado = girar_ruleta()  # Giramos la ruleta
            print('Has caído en:', resultado)

            jugador = jugadores[turno_actual]
            solucion = comprobar_gajo(jugador, resultado, panel_original, pista)  # Comprobamos el gajo resultante

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
            ganador()  # Mostramos al jugador que ha ganado
            break  # Si no queremos jugar otra partida, salimos del bucle

#-----------------------------------------------------------------------------------------

### EJECUTAR JUEGO
        
if __name__ == "__main__":
    juego_ruleta()
