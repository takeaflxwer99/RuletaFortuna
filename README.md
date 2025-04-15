# 🎯 La Ruleta de la Suerte 🎡

Una versión en Python del famoso programa de televisión **"La Ruleta de la Suerte"**. Este juego permite a 1 o 3 jugadores competir resolviendo paneles, ganando o perdiendo puntos según lo que les toque en la ruleta.

---

## 🧩 Introducción

Este programa simula una ruleta de la fortuna. En cada turno, los jugadores giran la ruleta y eligen una letra para intentar resolver el panel. Dependiendo del resultado, ganarán o perderán puntos. ¡El jugador con más puntos al final será el ganador!

---

## ⚙️ Requisitos del sistema

- Python **3.8 o superior**
- Sistema operativo: **Windows**, **macOS** o **Linux**
- Archivos necesarios:
  - `RULETA.py`
  - `panel_pistas.txt` (debe estar en la misma carpeta que el archivo Python)

---

## 🛠️ Instalación y ejecución

1. Abre **Thonny** (u otro entorno Python).
2. Abre el archivo `RULETA.py`.
3. Pulsa **Ejecutar** (▶️).
4. ¡El juego comenzará automáticamente en la consola!

---

## 👤 Modos de juego

Al iniciar el juego, podrás elegir entre dos modos:

- `1`: **Modo de un solo jugador**
  - Introduce tu nombre.
  - Juegas tú solo con una ruleta simplificada.
- `multi`: **Modo multijugador (3 jugadores)**
  - Los nombres son `jugador1`, `jugador2`, `jugador3`.
  - Los turnos y la puntuación se gestionan entre todos.

---

## 🎮 Cómo se juega

- Se elige aleatoriamente al jugador que empieza.
- En cada turno:
  - Pulsa **ENTER** para girar la ruleta.
  - Escribe una letra para intentar descubrir la frase.
  - Si aparece un gajo especial:
    - **Puntuación**: Sumas puntos si aciertas.
    - **Pierde turno**: Pierdes turno, no puntos.
    - **Quiebra**: Pierdes turno y puntos.
    - **Me lo quedo**: Robas puntos de otro jugador (solo multijugador).
    - **Se lo doy**: Das tus puntos a otro jugador (solo multijugador).
- Para resolver el panel, escribe la frase completa.
- Al final de cada ronda, puedes elegir si seguir o no con otro panel.
- El juego reconoce entradas en mayúsculas o minúsculas sin problema.

---

## ⌨️ Controles

| Acción               | Qué hacer                                 |
|----------------------|--------------------------------------------|
| Girar ruleta         | Pulsar ENTER                              |
| Elegir letra         | Escribir una letra y pulsar ENTER         |
| Resolver panel       | Escribir la frase completa                |
| Robar/Dar puntos     | Escribir el nombre del otro jugador       |
| Seguir jugando       | Escribir `si` o `no`                      |

---

## 🧑‍🤝‍🧑 Jugadores

### Modo un jugador:
- Se introduce un nombre personalizado.
- Solo participa una persona.

### Modo multijugador:
- Nombres fijos: `jugador1`, `jugador2`, `jugador3`.
- Todos empiezan con **0 puntos**.
- El turno inicial es aleatorio. Los turnos siguen este orden cíclico:
  `jugador1 → jugador2 → jugador3 → jugador1 → ...`

---

## 🧪 Testing y solución de problemas

Este programa ha sido probado con **pytest** usando técnicas como **mocking** para simular entradas y resultados aleatorios.

### ✔️ Casos probados:
- Selección de frases y pistas
- Manejo de archivo inexistente
- Validación de letras y frases
- Resultados de ruleta (puntos, especiales)
- Cambios de turno y puntuaciones
- Condiciones de fin de juego

### 🛠️ Problemas comunes y soluciones

| Problema                          | Posible solución                                                     |
|----------------------------------|----------------------------------------------------------------------|
| El juego no arranca              | Verifica que `panel_pistas.txt` esté en la misma carpeta.           |
| No aparecen letras               | Escribe **una sola letra** sin símbolos ni números.                 |
| Juego se cierra solo             | Puede que ya se jugaron todos los paneles. Reinicia o añade más.    |
| No reconoce al jugador           | Usa exactamente: `jugador1`, `jugador2`, `jugador3` (en multi).     |
| Frase incorrecta al resolver     | Se detecta como fallo y se pasa el turno.                           |

---

## 🧪 Cobertura de Testing Automatizado

El proyecto cuenta con una **suite de tests automatizados en `pytest`** que cubre todos los aspectos funcionales del juego.

### 🔬 ¿Qué se ha probado?

#### 🎯 Paneles
- ✅ Lectura de frases y pistas válidas desde archivo
- ✅ Manejo de archivos inexistentes
- ✅ Evita repetir frases jugadas

#### 🔤 Letras y frases
- ✅ Registro correcto de letras acertadas
- ✅ Rechazo de letras repetidas o incorrectas
- ✅ Comparación de frases ignorando mayúsculas y espacios

#### 🎡 Ruleta
- ✅ Resultados aleatorios validados con `mock`
- ✅ Casillas especiales:
  - Puntuación (25, 50, 100, etc.)
  - Pierde turno
  - Quiebra
  - Me lo quedo
  - Se lo doy

#### 🧮 Puntuaciones
- ✅ Suma/resta correcta de puntos
- ✅ Transferencias entre jugadores
- ✅ Reinicio a 0 en “Quiebra”

#### 🔁 Turnos
- ✅ Turno inicial aleatorio
- ✅ Ciclo continuo de turnos (jugador1 → jugador2 → jugador3 → ...)
- ✅ Gestión tras fallo o acierto

#### 🏁 Final de partida
- ✅ Reconocimiento de victoria con mensaje final
- ✅ Gestión de empates
- ✅ Confirmación de cierre del juego cuando se decide no continuar

#### 🧪 Técnicas de testing utilizadas
- `mock_open` para simular archivos
- `patch` para modificar funciones como `random.choice`
- `capsys` para verificar salidas por consola
- `monkeypatch` para simular entradas del usuario
- `fixture` para reiniciar variables globales antes de cada prueba

---

> ✅ **Resultado:** Cobertura total asegurada. Todos los caminos lógicos del juego han sido validados, incluidos los errores esperados y los flujos especiales.

---

## 📌 Conclusiones

Este proyecto fue una gran oportunidad para aprender a desarrollar un juego sin interfaz gráfica usando Python. Nos dividimos las funciones, desde la ruleta hasta la lógica de turnos y puntuaciones, y las integramos en una función principal. Usamos `pytest` para verificar la funcionalidad del juego.

### Dificultades superadas:
- 🔁 Controlar turnos correctamente con:
  ```python
  turno_actual = (turno_actual + 1) % len(jugadores)
