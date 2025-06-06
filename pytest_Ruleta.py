# test_juego_ruleta.py

import pytest
import random
from unittest.mock import mock_open, patch
from RULETA import (
    seleccionar_frase,
    mostrar_panel,
    elegir_jugador,
    girar_ruleta,
    comprobar_letra,
    comprobar_frase,
    comprobar_gajo,
    sumar_puntos,
    ganador,
    puntuaciones,
    jugadores,
    letras_acertadas,
    paneles_jugados
)

# ---------------------------
# Fixtures y preparación
# ---------------------------
@pytest.fixture(autouse=True)
def reset_globales():
    puntuaciones.clear()
    puntuaciones.update({'jugador1': 0, 'jugador2': 0, 'jugador3': 0})
    letras_acertadas.clear()
    paneles_jugados.clear()
    random.seed(42)
    jugadores.clear()
    jugadores.extend(['jugador1', 'jugador2', 'jugador3'])

# ---------------------------
# solo un jugador
# ---------------------------
def test_juego_un_jugador(monkeypatch):
    # Simula un solo jugador
    jugadores.clear()
    jugadores.append('jugador_unico')
    puntuaciones.clear()
    puntuaciones['jugador_unico'] = 0

    # Simulamos una ronda con entrada "A", no resolver
    inputs = iter(["A", "no"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    resultado = "50"
    sigue_jugando, cambio = comprobar_gajo('jugador_unico', resultado, "A B C", "Pista")

    assert sigue_jugando is True
    assert puntuaciones['jugador_unico'] == 50

# ---------------------------
# seleccionar_frase
# ---------------------------
def test_seleccionar_frase_sin_archivo():
    with pytest.raises(FileNotFoundError):
        seleccionar_frase("archivo_inexistente.txt")

@patch("builtins.open", new_callable=mock_open, read_data="FRASE1|Pista1\nFRASE2|Pista2\n")
def test_seleccionar_frase_valida(mock_file):
    frase, pista = seleccionar_frase("dummy.txt")
    assert frase == "FRASE1"
    assert pista == "Pista1"
    assert "FRASE1" in paneles_jugados

# ---------------------------
# comprobar_letra
# ---------------------------
def test_comprobar_letra_existente():
    assert comprobar_letra("A", "A B C", letras_acertadas) is True
    assert letras_acertadas == {"A": 1}

def test_comprobar_letra_inexistente():
    assert comprobar_letra("X", "A B C", letras_acertadas) is False
    assert letras_acertadas == {}

# ---------------------------
# comprobar_frase
# ---------------------------
def test_comprobar_frase_correcta():
    assert comprobar_frase("HOLA MUNDO", "hola mundo") is True

def test_comprobar_frase_incorrecta():
    assert comprobar_frase("HOLA MUNDO", "adios mundo") is False

# ---------------------------
# sumar_puntos
# ---------------------------
def test_sumar_puntos_numericos():
    sumar_puntos('jugador1', '100', 'jugador2')
    assert puntuaciones['jugador1'] == 100

def test_sumar_puntos_quiebra():
    puntuaciones['jugador1'] = 150
    sumar_puntos('jugador1', 'Quiebra', '')
    assert puntuaciones['jugador1'] == 0

def test_sumar_puntos_robo():
    puntuaciones['jugador2'] = 50
    sumar_puntos('jugador1', 'Me lo quedo', 'jugador2')
    assert puntuaciones['jugador1'] == 50
    assert puntuaciones['jugador2'] == 0

def test_sumar_puntos_donacion():
    puntuaciones['jugador1'] = 70
    sumar_puntos('jugador1', 'Se lo doy', 'jugador2')
    assert puntuaciones['jugador1'] == 0
    assert puntuaciones['jugador2'] == 70

# ---------------------------
# girar_ruleta
# ---------------------------
@patch("random.choice")
def test_girar_ruleta(mock_choice):
    import RULETA
    RULETA.opciones_ruleta = ['25', '50', '100']
    mock_choice.return_value = "100"
    assert girar_ruleta() == "100"

# ---------------------------
# elegir_jugador
# ---------------------------
def test_elegir_jugador():
    random.seed(0)
    assert elegir_jugador() in [0, 1, 2]

# ---------------------------
# comprobar_gajo
# ---------------------------
def test_comprobar_gajo_pierde_turno(capsys):
    resultado = "Pierde turno"
    sigue_jugando, cambio = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert sigue_jugando is True and cambio is True
    captured = capsys.readouterr()
    assert "pierde su turno" in captured.out.lower()

def test_comprobar_gajo_quiebra(capsys):
    puntuaciones['jugador1'] = 80
    resultado = "Quiebra"
    sigue_jugando, cambio = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert puntuaciones['jugador1'] == 0
    assert sigue_jugando is True and cambio is True

def test_comprobar_gajo_me_lo_quedo(monkeypatch):
    inputs = iter(["A", "jugador2", "no"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    puntuaciones['jugador2'] = 100
    resultado = "Me lo quedo"
    sigue_jugando, cambio = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert puntuaciones['jugador1'] == 100
    assert puntuaciones['jugador2'] == 0
    assert sigue_jugando is True

def test_comprobar_gajo_se_lo_doy(monkeypatch):
    inputs = iter(["jugador2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    puntuaciones['jugador1'] = 60
    resultado = "Se lo doy"
    sigue_jugando, cambio = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert puntuaciones['jugador1'] == 0
    assert puntuaciones['jugador2'] == 60
    assert sigue_jugando is True

def test_comprobar_gajo_letra_acertada(monkeypatch):
    inputs = iter(["A", "no"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = "50"
    sigue_jugando, cambio = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert puntuaciones['jugador1'] == 50
    assert sigue_jugando is True

def test_comprobar_gajo_resolver_correcto(monkeypatch, capsys):
    inputs = iter(["A", "si", "A B C"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = "50"
    sigue_jugando, cambio = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    captured = capsys.readouterr()
    assert sigue_jugando is False
    assert "has resuelto el panel" in captured.out.lower()

# ---------------------------
# ganador
# ---------------------------
def test_ganador_unico(capsys):
    puntuaciones.update({'jugador1': 100, 'jugador2': 50, 'jugador3': 70})
    ganador()
    captured = capsys.readouterr()
    assert "ha ganado el jugador1" in captured.out.lower()

def test_ganador_empate(capsys):
    puntuaciones.update({'jugador1': 100, 'jugador2': 100, 'jugador3': 70})
    ganador()
    captured = capsys.readouterr()
    assert "hay empate entre" in captured.out.lower()
