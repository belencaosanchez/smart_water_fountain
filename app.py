from flask import Flask, render_template, redirect, url_for
from gpiozero import AngularServo, LED, MCP3008
from gpiozero.pins.pigpio import PiGPIOFactory
import threading
import time

factory = PiGPIOFactory()

app = Flask(__name__)

# Configuración de hardware
# Servo conectado a GPIO22 (BCM22)
servo = AngularServo(22, min_angle=-90, max_angle=90, pin_factory=factory)
servo.angle = 90  # Inicialmente ABIERTO

# LEDs (usando pigpio para evitar conflictos)
blue_led = LED(25, pin_factory=factory)   # Se usará para indicar condición de luz
green_led = LED(23, pin_factory=factory)  # Se usará para indicar condición de distancia
red_led = LED(24, pin_factory=factory)    # Se encenderá cuando se cierre o si la botella está llena

blue_led.off()
green_led.off()
red_led.off()

# Sensores (MCP3008)
distance_sensor = MCP3008(channel=0)  # Distancia
light_sensor = MCP3008(channel=4)     # Luz
weight_sensor = MCP3008(channel=2)    # Peso

# Variables de estado
run_loop = False
botella_llena = False
log_messages = []
loop_thread = None
last_state = None  # Para almacenar el último mensaje de estado

def set_log(msg: str):
    """Actualiza el log solo si el mensaje es distinto al último registrado."""
    global log_messages, last_state
    if msg != last_state:
        log_messages.append(msg)
        last_state = msg
        print(msg)

def sensor_loop():
    global run_loop, botella_llena, log_messages, last_state
    # Al iniciar, mostramos un mensaje inicial
    set_log("SISTEMA INICIADO.")
    
    while run_loop:
        # Lectura de sensores
        distance_v = distance_sensor.voltage
        light_v = light_sensor.voltage
        weight_v = weight_sensor.voltage

        # Lógica de control con LEDs
        if not botella_llena:
            if (distance_v < 3.0) or (1.0 <= light_v <= 1.3):
                # Condición para abrir el servo
                servo.angle = 90
                # Prioriza: si el sensor de distancia se cumple, enciende el LED verde; si no, el azul
                if distance_v < 3.0:
                    green_led.on()
                    blue_led.off()
                else:
                    blue_led.on()
                    green_led.off()
                red_led.off()
                state_message = "SERVO ABIERTO"

                # Si se detecta peso, se considera que la botella está llena
                if weight_v >= 2.45:
                    botella_llena = True
                    state_message = "SERVO CERRADO (Botella llena)"
            else:
                # Si no se cumple la condición, cierra el servo y apaga LEDs
                servo.angle = -90
                blue_led.off()
                green_led.off()
                red_led.off()
                state_message = "SERVO CERRADO"
        else:
            # Si ya está llena, forzamos el cierre y se enciende el LED rojo
            servo.angle = -90
            blue_led.off()
            green_led.off()
            red_led.on()
            state_message = "SERVO CERRADO (Botella llena)"
        
        # Actualizamos el log solo si cambia el mensaje
        set_log(state_message)
        
        time.sleep(0.3)

    # Al salir del bucle (cuando se pulse "ACABAR")
    servo.angle = -90
    blue_led.off()
    green_led.off()
    red_led.on()
    set_log("SERVO CERRADO")
    set_log("SISTEMA FINALIZADO.")
    
    time.sleep(2)
    # Finalmente, se vacía el log
    log_messages = []
    last_state = None

@app.route('/')
def index():
    return render_template("index.html", logs=log_messages)

@app.route('/empezar')
def empezar():
    global run_loop, loop_thread, log_messages, botella_llena, last_state
    if not run_loop:
        # Reiniciamos variables de estado y log
        log_messages = []
        last_state = None
        botella_llena = False
        run_loop = True
        loop_thread = threading.Thread(target=sensor_loop)
        loop_thread.start()
    return redirect(url_for("index"))

@app.route('/acabar')
def acabar():
    global run_loop
    run_loop = False
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
