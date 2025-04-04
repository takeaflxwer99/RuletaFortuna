import unittest
from unittest.mock import patch, mock_open
import RULETA

class TestRuleta(unittest.TestCase):

    def setUp(self):
        # Reiniciar variables globales antes de cada prueba
        RULETA.puntuaciones = {
            'jugador1': 0,
            'jugador2': 0,
            'jugador3': 0
        }
        RULETA.letras_acertadas = {}
        RULETA.turno_actual = 0  # Asegurar que el turno empiece en 0

    @patch("builtins.open", new_callable=mock_open, read_data="FRASE DE PRUEBA|Pista\n")
    def test_seleccionar_frase(self, mock_file):
        frase, pista = RULETA.seleccionar_frase("panel_pistas.txt")
        self.assertEqual(frase, "FRASE DE PRUEBA")
        self.assertEqual(pista, "Pista")

    def test_comprobar_letra(self):
        # Caso de acierto
        self.assertTrue(RULETA.comprobar_letra('A', "FRASE A", RULETA.letras_acertadas))
        self.assertIn('A', RULETA.letras_acertadas)
        # Caso de fallo
        self.assertFalse(RULETA.comprobar_letra('Z', "FRASE A", RULETA.letras_acertadas))

    def test_comprobar_frase(self):
        self.assertTrue(RULETA.comprobar_frase("FRASE", "frase"))
        self.assertFalse(RULETA.comprobar_frase("FRASE", "incorrecta"))

    def test_sumar_puntos(self):
        # Suma normal
        RULETA.sumar_puntos('jugador1', '100', '')
        self.assertEqual(RULETA.puntuaciones['jugador1'], 100)
        # Quiebra
        RULETA.sumar_puntos('jugador1', 'Quiebra', '')
        self.assertEqual(RULETA.puntuaciones['jugador1'], 0)
        # Me lo quedo
        RULETA.puntuaciones['jugador2'] = 50
        RULETA.sumar_puntos('jugador1', 'Me lo quedo', 'jugador2')
        self.assertEqual(RULETA.puntuaciones['jugador1'], 50)
        self.assertEqual(RULETA.puntuaciones['jugador2'], 0)
        # Se lo doy
        RULETA.puntuaciones['jugador1'] = 30
        RULETA.sumar_puntos('jugador1', 'Se lo doy', 'jugador2')
        self.assertEqual(RULETA.puntuaciones['jugador1'], 0)
        self.assertEqual(RULETA.puntuaciones['jugador2'], 30)

    @patch('builtins.input', side_effect=['A', 'no'])
    @patch('RULETA.girar_ruleta', return_value='50')
    def test_comprobar_gajo_letra_acertada(self, mock_ruleta, mock_input):
        frase = "FRASE A"
        pista = "Pista"
        resultado = RULETA.comprobar_gajo('jugador1', '50', frase, pista)
        self.assertTrue(resultado)
        self.assertEqual(RULETA.puntuaciones['jugador1'], 50)

    @patch('builtins.input', side_effect=['Z', 'no'])
    @patch('RULETA.girar_ruleta', return_value='50')
    def test_comprobar_gajo_letra_fallada(self, mock_ruleta, mock_input):
        frase = "FRASE A"
        pista = "Pista"
        resultado = RULETA.comprobar_gajo('jugador1', '50', frase, pista)
        self.assertTrue(resultado)
        self.assertEqual(RULETA.turno_actual, 1)  # Verifica que el turno cambió

    @patch('builtins.input', side_effect=['A', 'si', 'FRASE A'])
    @patch('RULETA.girar_ruleta', return_value='50')
    def test_comprobar_gajo_resolver_correcto(self, mock_ruleta, mock_input):
        frase = "FRASE A"
        pista = "Pista"
        resultado = RULETA.comprobar_gajo('jugador1', '50', frase, pista)
        self.assertFalse(resultado)  # El juego termina

    @patch('builtins.input', side_effect=['A', 'si', 'INCORRECTA'])
    @patch('RULETA.girar_ruleta', return_value='50')
    def test_comprobar_gajo_resolver_incorrecto(self, mock_ruleta, mock_input):
        frase = "FRASE A"
        pista = "Pista"
        resultado = RULETA.comprobar_gajo('jugador1', '50', frase, pista)
        self.assertTrue(resultado)
        self.assertEqual(RULETA.turno_actual, 1)

if __name__ == "__main__":
    unittest.main()