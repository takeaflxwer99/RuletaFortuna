# Ruleta de la Fortuna - GTDM, Programación A1. 

import random
import time

### VARIABLES PRINCIPALES

# Inicialmente vacía. Se rellena dependiendo del modo (1 jugador o multijugador)
jugadores = []
# Creamos un diccionario que guarde el dinero/puntuacion de cada jugador
puntuaciones = {}
# Creamos otro diccionario que guarde las letras acertadas
letras_acertadas = {}
# Escribimos aparte en un documento de tipo '.txt' las frases y pistas que hemos elegido
fichero_frases = "panel_pistas.txt"
# Cremos una lista que guarde los paneles que ya han salido para no repetirlos
paneles_jugados = []
# Variable que indica de quién es el turno actual
turno_actual = 0

#-----------------------------------------------------------------------------------------

### FUNCIONES RELACIONADAS CON EL PANEL

# Seleccionamos aleatoriamente una frase y su pista desde el archivo
def seleccionar_frase(fichero):
    # Abrimos el archivo en el que hemos guardado las frases y pistas
    with open(fichero, 'r', encoding='utf-8') as fich:
        # Leemos todas las líneas del archivo
        lineas = fich.readlines()
    # Filtramos solo las líneas que contienen el símbolo '|'
    lineas_validas = [l for l in lineas if '|' in l]
    # Seleccionamos las frases que todavía no se han jugado
    disponibles = [l for l in lineas_validas if l.strip().split('|')[0].upper() not in paneles_jugados]
    # Si no hay frases disponibles, se han jugado todas y el juego termina
    if not disponibles:
        print("\n¡Se han jugado todos los paneles! Fin del juego.")
        exit()
    # Seleccionamos aleatoriamente una línea disponible y la separamos en frase y pista
    frase, pista = random.choice(disponibles).strip().split('|')
    # Añadimos la frase ya jugada para no repetirla
    paneles_jugados.append(frase.upper())
    return frase.upper(), pista

# Mostramos el panel con las letras acertadas hasta el momento
def mostrar_panel(frase, letras_acertadas, pista):
    # Mostramos una letra si ha sido acertada; si no, mostramos '_'
    panel_mostrado = [letra if letra in letras_acertadas or letra == ' ' else '_' for letra in frase]
    # Mostramos visualmente el panel con la pista y las letras adivinadas
    print("\n" + "="*40)
    print(f"📌  PISTA: {pista}")
    print("\n>   PANEL:")
    print("\n   " + " ".join(panel_mostrado))
    print("\n" + "="*40)

#-----------------------------------------------------------------------------------------

### FUNCIONES PARA GUARDAR RESULTADOS Y ACTUALIZAR RANKING

# Guarda cada panel resuelto en un archivo para llevar un historial de partidas
def guardar_panel_resuelto(jugador, frase):
    with open("historial_partidas.txt", "a", encoding="utf-8") as f:
        f.write(f"{jugador} resolvió el panel: '{frase}'\n")

# Actualiza el ranking acumulado de paneles resueltos en un archivo
def actualizar_ranking(jugador):
    ranking = {}
    # Intentamos leer el archivo de ranking existente
    try:
        with open("ranking_jugadores.txt", "r", encoding="utf-8") as f:
            for linea in f:
                if ":" in linea:
                    partes = linea.strip().split(":")
                    if len(partes) == 2:
                        nombre, puntuacion = partes
                        ranking[nombre] = int(puntuacion)
    except FileNotFoundError:
        pass  # Si no existe, se crea desde cero

    # Sumamos 1 panel resuelto para el jugador
    ranking[jugador] = ranking.get(jugador, 0) + 1

    # Escribimos el ranking actualizado en el archivo
    with open("ranking_jugadores.txt", "w", encoding="utf-8") as f:
        for nombre, puntos in ranking.items():
            f.write(f"{nombre}:{puntos}\n")

# Función para mostrar el ranking acumulado
def mostrar_ranking():
    print("\n🏆 RANKING ACUMULADO DE PANELISTAS 🏆")
    try:
        with open("ranking_jugadores.txt", "r", encoding="utf-8") as f:
            contenido = f.readlines()
            if not contenido:
                print("No hay ranking registrado aún.")
                return False
            else:
                # Variable para comprobar si hay líneas con el formato correcto
                ranking_valido = False
                for linea in contenido:
                    # Verificamos que la línea no esté vacía y tenga el formato correcto
                    if ":" in linea:
                        try:
                            nombre, puntos = linea.strip().split(":")
                            print(f"{nombre}: {puntos} paneles resueltos")
                            ranking_valido = True
                        except ValueError:
                            continue  # Si no se puede separar correctamente, saltamos la línea
                    else:
                        continue  # Si no hay ":", seguimos con la siguiente línea
                if not ranking_valido:
                    print("No hay ranking válido registrado aún.")
                return True
    except FileNotFoundError:
        print("No hay ranking registrado aún.")
        return False



#-----------------------------------------------------------------------------------------

### FUNCIONES RELACIONADAS CON EL JUEGO

# Elegimos aleatoriamente al jugador que empieza
def elegir_jugador():
    print('\nEligiendo jugador...')
    turno = random.randint(0, len(jugadores) - 1)  # Se escoge un jugador al azar
    time.sleep(2)  # Simula una pausa de suspenso
    return turno

# Simulamos el giro de la ruleta y devolvemos el resultado
def girar_ruleta():
    # Se elige aleatoriamente una opción entre los posibles valores del gajo
    resultado = random.choice(opciones_ruleta)
    time.sleep(2)
    return resultado

# Verificamos si la letra está en la frase y no ha sido dicha antes
def comprobar_letra(letra, frase, letras_acertadas):
    letra = letra.upper()
    if letra in letras_acertadas:
        print("Esa letra ya se ha dicho. Intenta con otra distinta.")
        return False
    if letra in frase:
        # Si es correcta, se añade al registro de letras acertadas
        letras_acertadas[letra] = letras_acertadas.get(letra, 0) + 1
        return True
    return False

# Comprobamos si la frase que se ha introducido es correcta
def comprobar_frase(frase_correcta, frase_usuario):
    # Comparamos ambas frases ignorando mayúsculas y espacios extra
    return frase_correcta.strip().upper() == frase_usuario.strip().upper()

# Sumamos o restamos puntos según el resultado de la ruleta
def sumar_puntos(jugador, resultado, otrojugador):
    if resultado.isdigit():
        # Si es un valor numérico, sumamos esa cantidad
        puntos = int(resultado)
        puntuaciones[jugador] += puntos
        print(f"\n{jugador} ha sumado {puntos} puntos.")
    elif resultado == "Quiebra":
        # Si es Quiebra, el jugador pierde todo
        puntuaciones[jugador] = 0 
        print(f"\n{jugador} ha perdido todo su dinero.")
    elif resultado == "Me lo quedo":
        # El jugador roba todos los puntos de otro jugador
        puntuaciones[jugador] += puntuaciones[otrojugador]
        puntuaciones[otrojugador] = 0
        print(f"\n{jugador} ha robado los puntos de {otrojugador}.")
    elif resultado == "Se lo doy":
        # El jugador entrega todos sus puntos al otro jugador
        puntuaciones[otrojugador] += puntuaciones[jugador]
        puntuaciones[jugador] = 0
        print(f"\n{jugador} ha dado sus puntos a {otrojugador}.")
        
# Comprobamos qué tipo de casilla (dinero o especial) ha salido y qué hacer según el caso

def comprobar_gajo(jugador, resultado, frase, pista):
    global turno_actual

    def pedir_letra_valida():
        while True:
            letra = input('\n¿Qué letra quieres? ').strip().upper()
            if len(letra) != 1 or not letra.isalpha():
                print("Por favor, escribe solo una letra.")
            elif letra in letras_acertadas:
                print("Esa letra ya se ha dicho. Intenta con otra distinta.")
            else:
                return letra

    if resultado == 'Me lo quedo':
        letra = pedir_letra_valida()
        if comprobar_letra(letra, frase, letras_acertadas):
            mostrar_panel(frase, letras_acertadas, pista)
            while True:
                otrojugador_input = input('\n¿A qué jugador quieres robarle los puntos? ')
                otrojugador = otrojugador_input.lower().replace(" ", "")
                if otrojugador not in jugadores:
                    print("Entrada no válida. Solo puedes elegir:", ", ".join(jugadores))
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
                    guardar_panel_resuelto(jugador, frase)
                    actualizar_ranking(jugador)
                    return False, False
                else:
                    print('\nNo era esa la respuesta... ¡pierdes el turno!')
                    turno_actual = (turno_actual + 1) % len(jugadores)
                    return True, True
            else:
                return True, False
        else:
            print("\nEsa letra no está en el panel.")
            turno_actual = (turno_actual + 1) % len(jugadores)
            return True, True

    elif resultado == 'Se lo doy':
        print(f"\n{jugador} tiene que darle los puntos a otro jugador y pierde su turno.")
        while True:
            otrojugador_input = input('\n¿A qué jugador quieres darle tus puntos? ')
            otrojugador = otrojugador_input.lower().replace(" ", "")
            if otrojugador not in jugadores:
                print("Entrada no válida. Solo puedes elegir:", ", ".join(jugadores))
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

    else:  # Caso normal de dinero
        letra = pedir_letra_valida()
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
                    guardar_panel_resuelto(jugador, frase)
                    actualizar_ranking(jugador)
                    return False, False
                else:
                    print('\nNo era esa la respuesta... ¡pierdes el turno!')
                    turno_actual = (turno_actual + 1) % len(jugadores)
                    return True, True
            else:
                return True, False
        else:
            print("\nEsa letra no está en el panel.")
            turno_actual = (turno_actual + 1) % len(jugadores)
            return True, True


#-----------------------------------------------------------------------------------------

### FUNCION PARA MOSTRAR AL GANADOR

def ganador():
    # Buscamos la puntuación más alta entre todos los jugadores
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

def juego_ruleta():
    global turno_actual, jugadores, puntuaciones, opciones_ruleta

    print("\n¡Bienvenido a la Ruleta de la Fortuna!")

    while True:
        print("\n¿Qué quieres hacer?")
        print("1. Ver ranking")
        print("2. Jugar (1 jugador o multijugador)")
        print("3. Salir")
        eleccion = input("Elige una opción (1/2/3): ").strip()

        if eleccion == "1":
            hay_datos = mostrar_ranking()
            if not hay_datos:
                continue
            while True:
                siguiente = input("\n¿Quieres jugar o salir? (jugar/salir): ").strip().lower()
                if siguiente in ['jugar']:
                    break
                elif siguiente in ['salir']:
                    print("\n¡Hasta la próxima!")
                    return
                else:
                    print("Opción no válida. Escribe 'jugar' o 'salir'.")
            # Si elige jugar, rompemos este bucle y seguimos con el juego
            break
        elif eleccion == "2":
            break
        elif eleccion == "3":
            print("\n¡Hasta la próxima!")
            return
        else:
            print("Opción no válida. Por favor, elige 1, 2 o 3.")

    # Preguntamos hasta que se introduzca una opción válida: "1" o "multi"
    while True:
        modo = input("¿Quieres jugar en modo de 1 jugador o multijugador? (1/multi): ").strip().lower()
        if modo in ["1", "multi","Multi","MULTI"]:
            break
        else:
            print("Por favor, escribe solo '1' para un jugador o 'multi' para multijugador.")
    
    if modo == "1":
        nombre = input("Escribe tu nombre: ").strip().lower()
        jugadores = [nombre]
        puntuaciones = {nombre: 0}

        # Ruleta reducida para el modo de un jugador
        opciones_ruleta = ['25', '50', '100', '150', 'Quiebra', 'Pierde turno']
    else:
        jugadores = ['jugador1', 'jugador2', 'jugador3']
        puntuaciones = {j: 0 for j in jugadores}
        opciones_ruleta = ['0', '25', '50', '75', '100', '150', 'Pierde turno', 'Quiebra', 'Me lo quedo', 'Se lo doy']

    while True:
        letras_acertadas.clear()  # Reiniciamos las letras acertadas
        panel_original, pista = seleccionar_frase(fichero_frases)  # Seleccionamos nuevo panel
        turno_actual = elegir_jugador()  # Elegimos quién empieza
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
    
        if otra_partida not in ['si', 'sí', 'si', 'sí']:  # Si el jugador no quiere seguir jugando
            ver_ranking = input("¿Quieres ver el ranking actualizado? (sí/no): ").strip().lower()
            if ver_ranking in ['sí', 'si', 's']:
                # Llamamos a la función para mostrar el ranking
                mostrar_ranking()
        print("\n¡Gracias por jugar!")
        ganador()  # O lo que haga la función ganador()
        break  # Salimos del bucle y terminamos el juego

#-----------------------------------------------------------------------------------------

### EJECUTAR JUEGO

if __name__ == "__main__":
    juego_ruleta()
