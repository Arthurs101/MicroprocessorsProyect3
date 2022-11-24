import board
import busio
import adafruit_bmp280
import time
import I2C_LCD_driver

#instancia i2c con el mapeo del board configuarada para detectar el SCL y SDA del sensor
i2c = busio.I2C(board.SCL,board.SDA)

#crear el objeto de sensor, indicandole la dirección de la conecxión
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address = 0x76)

#configurar la lcd
mylcd = I2C_LCD_driver.lcd()

import RPi.GPIO as GPIO
import json
import Apimanager as api
RED = 20
GRN = 26
YLW = 21
BLUE= 19
LIGHT = 16
INF = 13#sensor infrarrojo

#diccionario con los datos
dataset = {
    'Temperatura(°C)' : [],
    'Temperatura(°F)' :[],
    'Temperatura(K)' :[],
    'Iluminacion':[]
    }

str_pad = " " * 16
header1 = "esperando activacion para medir datos"
subhdr =  "                usar sensor infrarojo"
header1= str_pad + header1
subhdr = str_pad + subhdr
#setup a los pines
GPIO.setmode(GPIO.BCM)
GPIO.setup(GRN, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YLW, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
#sensor de luz
GPIO.setup(LIGHT,GPIO.IN)
GPIO.setup(INF,GPIO.IN)

GPIO.output(BLUE,False)
GPIO.output(GRN,False)
GPIO.output(YLW, False)
GPIO.output(RED,False)
def LEDELECTOR(TEMP):
    #crear los rangos de temperatura a usar
    if(temp < 20):
        GPIO.output(BLUE,True)
        GPIO.output(GRN,False)
        GPIO.output(YLW, False)
        GPIO.output(RED,False)
    elif(temp >=21 and temp < 22):
        GPIO.output(GRN,True)
        GPIO.output(BLUE,False)
        GPIO.output(YLW, False)
        GPIO.output(RED,False)
    elif(temp >= 22.0 and temp < 24.0):
        GPIO.output(YLW, True)
        GPIO.output(BLUE,False)
        GPIO.output(GRN,False)
        GPIO.output(RED,False)
    elif(temp >= 24.0):
        GPIO.output(YLW, False)
        GPIO.output(RED,True)
        GPIO.output(BLUE,False)
        GPIO.output(GRN,False)
        
while GPIO.input(INF) != GPIO.LOW:
    for i in range (0, len(header1)):
        lcd_text = header1[i:(i+16)]
        text2 = subhdr[i:(i+16)]
        mylcd.lcd_display_string(lcd_text,1)
        mylcd.lcd_display_string(text2,2)
        mylcd.lcd_display_string(str_pad,1)
        mylcd.lcd_display_string(str_pad,2)
    time.sleep(1)
    
mylcd.lcd_clear()
mylcd.lcd_display_string("Empezando",1)
mylcd.lcd_display_string("Espera...",2)
time.sleep(4)
mylcd.lcd_clear()

while GPIO.input(INF) != GPIO.LOW:
    temp = round(sensor.temperature,2)
    light = not(GPIO.input(LIGHT))
    mylcd.lcd_display_string(f'Temp: {temp} C' , 1)
    mylcd.lcd_display_string(f'Luz: {light}' , 2)
    LEDELECTOR(temp)
    dataset['Temperatura(°C)'].append(temp)
    dataset['Temperatura(°F)'].append(0)
    dataset['Temperatura(K)'].append(0)
    dataset['Iluminacion'].append(light)
    time.sleep(0.5)
    mylcd.lcd_clear()
api.sendElements(dataset)
mylcd.lcd_display_string("datos",1)
mylcd.lcd_display_string("guardados",2)
time.sleep(1)
mylcd.lcd_clear()

        
GPIO.output(BLUE,False)
GPIO.output(GRN,False)
GPIO.output(YLW, False)
GPIO.output(RED,False)
