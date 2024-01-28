
import Adafruit_DHT
import I2C_LCD_driver
import RPi.GPIO as GPIO
import signal
import sys
import time

L1 = 25
L2 = 12
L3 = 13
L4 = 19

C1 = 17
C2 = 18
C3 = 27
C4 = 22

UV1 = 10
UV2 = 9
UV3 = 11
UV4 = 6

LED_GPIO = 24
BUTTON_GPIO = 26
DOOR_GPIO = 5
SENSOR_GPIO = 23  # DTH22
mylcd = I2C_LCD_driver.lcd()

# Definir puertos I/O
def gpio_ports():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DOOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(LED_GPIO, GPIO.OUT)
    GPIO.setup(UV1, GPIO.OUT)
    GPIO.setup(UV2, GPIO.OUT)
    GPIO.setup(UV3, GPIO.OUT)
    GPIO.setup(UV4, GPIO.OUT)


def signal_handler(sig, frame):
    GPIO.cleanup()
    mylcd.lcd_clear()
    sys.exit(0)

#Funcion pulsador de apagado
def button_shutdown_callback(channel):
    onLamps(0)
    mylcd.lcd_clear()
    mylcd.lcd_display_string("DesconEPPs vl.0", 1)
    mylcd.lcd_display_string("Shutting down...", 2)
    shut_down()
        
#Funcion bucle encendido de luces UVC
def lamps_loop(state):
    if GPIO.input(DOOR_GPIO):
        mylcd.lcd_clear()
        mylcd.lcd_display_string("DesconEPPs v1.0", 1)
        mylcd.lcd_display_string("Starting...", 2)
        time.sleep(2)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Press a key", 1)
        mylcd.lcd_display_string("11 12 13 1A", 2)
        time.sleep(2)
        try:
            tecla1 = "X"
            while tecla1 == "X":
                tecla1 = readline(L1, ["1", "2", "3", "A"])
                if tecla1 != "X":
                    break
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("Application stopped!")

        if tecla1 == "1":
            lamp = 1
        elif tecla1 == "2":
            lamp = 2
        elif tecla1 == "3":
            lamp = 3
        elif tecla1 == "A":
            lamp = 4

        mylcd.lcd_clear()

        mylcd.lcd_display_string("Press a key", 1)
        mylcd.lcd_display_string("4 5 6 B", 2)
        time.sleep(2)
        try:
            tecla2 = "X"
            while tecla2 == "X":
                tecla2 = readline(L2, ["4", "5", "6", "B"])
                if tecla2 != "X":
                    break
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("Application stopped!")

        if tecla2 == "4":
            te = 1.5
        elif tecla2 == "5":
            te = 2
        elif tecla2 == "6":
            te = 5
        elif tecla2 == "B":
            te = 10

        mylcd.lcd_clear()
        mylcd.lcd_display_string("Lamps:%d %smin" % (lamp, te), 1)
        time.sleep(10)
        onLamps(lamp)
        start_time = time.time()
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, SENSOR_GPTO)
            mylcd.lcd_display_string("%0.1f%sC %0.1f%%" % (temperature, chr(223), humidity), 2)
            if (time.time() - start_time) > te * 60:
                break
        onLamps(0)
    else:
        # Mensaje de advertencia
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Warning:", 1)
        mylcd.lcd_display_string("Close the door!", 2)
        onLamps(0)

# Función para apagar
def shut_down():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

# Función para encender lámparas UVC
def onLamps(lamp):
    if lamp == 1:
        GPIO.output(UV1, GPIO.HIGH)
        GPIO.output(LED_GPIO, GPIO.HIGH)

    elif lamp == 2:
        GPIO.output(UV1, GPIO.HIGH)
        GPIO.output(UV2, GPIO.HIGH)
        GPIO.output(LED_GPIO, GPIO.HIGH)

    elif lamp == 3:
        GPIO.output(UV1, GPIO.HIGH)
        GPIO.output(UV2, GPIO.HIGH)
        GPIO.output(UV3, GPIO.HIGH)
        GPIO.output(LED_GPIO, GPIO.HIGH)

    elif lamp == 4:
        GPIO.output(UV1, GPIO.HIGH)
        GPIO.output(UV2, GPIO.HIGH)
        GPIO.output(UV3, GPIO.HIGH)
        GPIO.output(UV4, GPIO.HIGH)
        GPIO.output(LED_GPIO, GPIO.HIGH)

    elif lamp == 0:
        GPIO.output(UV1, GPIO.LOW)
        GPIO.output(UV2, GPIO.LOW)
        GPIO.output(UV3, GPIO.LOW)
        GPIO.output(UV4, GPIO.LOW)
        GPIO.output(LED_GPIO, GPIO.LOW)
        time.sleep(0.2)

# Función para leer teclado
def readline(line, characters):
def readline(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        t = characters[0]
    elif GPIO.input(C2) == 1:
        t = characters[1]
    elif GPIO.input(C3) == 1:
        t = characters[2]
    elif GPIO.input(C4) == 1:
        t = characters[3]
    else:
        t = "x"
    GPIO.output(line, GPIO.LOW)
    return t

# Programa principal
if __name__ == '__main__':
    gpio_ports()
    onLamps(0)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_shutdown_callback, bouncetime=100)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        lamps_loop(0)
    sys.exit(0)
