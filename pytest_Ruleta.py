# test_juego_ruleta.py
import pytest
from RULETA import (
    seleccionar_frase,
    mostrar_panel,
    elegir_jugador,
    girar_ruleta,
    comprobar_letra,
    comprobar_frase,
    comprobar_gajo,
    sumar_puntos,
    puntuaciones,
    jugadores,
    letras_acertadas,
    paneles_jugados
)

import random
from unittest.mock import mock_open, patch

# Fixture para resetear variables globales antes de cada test
@pytest.fixture(autouse=True)
def reset_globales():
    puntuaciones.clear()
    puntuaciones.update({'jugador1': 0, 'jugador2': 0, 'jugador3': 0})
    letras_acertadas.clear()
    paneles_jugados.clear()
    random.seed(42)  # Fijar semilla para resultados predecibles

# ---------------------------
# Tests para seleccionar_frase
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

# -------------------------
# Tests para comprobar_letra
# -------------------------
def test_comprobar_letra_existente():
    assert comprobar_letra("A", "A B C", letras_acertadas) is True
    assert letras_acertadas == {"A": 1}

def test_comprobar_letra_inexistente():
    assert comprobar_letra("X", "A B C", letras_acertadas) is False
    assert letras_acertadas == {}

# --------------------------
# Tests para comprobar_frase
# --------------------------
def test_comprobar_frase_correcta():
    assert comprobar_frase("HOLA MUNDO", "hola mundo") is True

def test_comprobar_frase_incorrecta():
    assert comprobar_frase("HOLA MUNDO", "adios mundo") is False

# ----------------------
# Tests para sumar_puntos
# ----------------------
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

# ----------------------
# Tests para girar_ruleta
# ----------------------
@patch("random.choice")
def test_girar_ruleta(mock_choice):
    mock_choice.return_value = "100"
    assert girar_ruleta() == "100"

# ----------------------
# Tests para elegir_jugador
# ----------------------
def test_elegir_jugador():
    random.seed(0)
    assert elegir_jugador() in [0, 1, 2]

# ----------------------
# Tests para comprobar_gajo (simulando inputs)
# ----------------------
def test_comprobar_gajo_pierde_turno(capsys):
    resultado = "Pierde turno"
    sigue_jugando = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert sigue_jugando is True
    captured = capsys.readouterr()
    assert "pierde su turno" in captured.out.lower()

def test_comprobar_gajo_letra_acertada(monkeypatch):
    inputs = iter(["A", "no"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = "50"
    sigue_jugando = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert sigue_jugando is True
    assert puntuaciones['jugador1'] == 50

def test_comprobar_gajo_resolver_correcto(monkeypatch, capsys):
    inputs = iter(["A", "si", "A B C"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = "50"
    sigue_jugando = comprobar_gajo('jugador1', resultado, "A B C", "Pista")
    assert sigue_jugando is False
    captured = capsys.readouterr()
    assert "¡Has resuelto el panel" in captured.out
