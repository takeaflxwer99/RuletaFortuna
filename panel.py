import random
fichero= "panel_pistas.txt"
paneles_jugados = []  # Frases ya jugadas
# función para leer frases desde un archivo y seleccionar una aleatoria
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