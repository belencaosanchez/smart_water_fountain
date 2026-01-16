# Sistema Automatizado de Llenado de Botellas de Agua

Este proyecto consiste en el desarrollo de una fuente de agua automatizada que
permite un llenado más eficiente de botellas, reduciendo el desperdicio de agua
y mejorando la experiencia del usuario.

El sistema está diseñado para su uso en entornos como universidades, donde es
frecuente el rellenado de botellas estándar de agua, permitiendo activar el
llenado de forma automática o manual.

---

## Descripción del Problema

En fuentes de agua convencionales, el usuario debe mantener presionado un botón
durante todo el proceso de llenado, lo que resulta poco eficiente y puede provocar
errores como sobrellenado o interrupciones imprecisas.

Este sistema propone una solución automatizada que permite iniciar el llenado con
un solo gesto y detenerlo automáticamente cuando la botella está llena, además de
ofrecer un modo de control manual.

---

## Descripción del Sistema

El sistema se basa en una Raspberry Pi que actúa como centro de control,
recibiendo información de distintos sensores y enviando señales a los actuadores.

Componentes principales:
- Servomotor: controla la apertura y cierre del grifo de agua.
- Sensor de fuerza (FSR): detecta cuándo la botella está llena.
- Sensor de distancia: detecta la presencia de la botella.
- Sensor de luz: funciona como pulsador en el modo manual.
- LED RGB: indica el estado del sistema.

El servomotor abre la válvula de agua cuando se cumplen las condiciones de
activación y la cierra automáticamente cuando se detecta que la botella está llena
o cuando el usuario lo solicita.

---

## Modos de Funcionamiento

### Modo Automático
- El sistema detecta la botella mediante el sensor de distancia.
- El grifo se abre automáticamente.
- El sensor de fuerza detecta cuándo la botella está llena.
- El sistema cierra el grifo y enciende el LED rojo.

### Modo Manual
- El usuario activa el sistema pulsando el sensor de luz.
- El grifo permanece abierto mientras el sensor esté pulsado.
- Al dejar de pulsar, el grifo se cierra.

---

## Indicadores LED

- **Verde**: apertura automática por detección de botella.
- **Azul**: apertura manual mediante el sensor de luz.
- **Rojo**: botella llena o sistema detenido.

---

## Interfaz Web

El sistema incluye una interfaz web desarrollada con Flask que permite controlar
el funcionamiento de la fuente de forma sencilla.

La interfaz cuenta con dos botones principales:
- **Empezar**: inicia el sistema de sensores y el control del servomotor.
- **Acabar**: detiene el proceso y cierra el grifo.

Además, se muestra el estado del sistema mediante mensajes de texto.

---

## Implementación

El control del sistema se ha desarrollado en Python utilizando la Raspberry Pi.
El programa lee continuamente los valores de los sensores y actúa sobre el
servomotor y los LEDs en función del modo de funcionamiento seleccionado.

Archivo principal:
- `app.py`

---

## Tecnologías Utilizadas

- Python
- Flask
- Raspberry Pi
- gpiozero
- Sensores analógicos y digitales
- Servomotor SG90
