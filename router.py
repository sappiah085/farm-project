from flask import Flask, Response, json, redirect, render_template, request
from piCameraModule import generate_frames
import RPi.GPIO as GPIO
import threading
import time
from sensor import read_sensor_data

IN1 = 17
IN2 = 22
IN3 = 23
IN4 = 24
ENA_A = 12
ENA_B = 25 

IN1A = 19
IN2A = 13
IN3A = 6
IN4A = 5

turningDSpeed = 50
turningLSpeed = 15


   
GPIO.setmode(GPIO.BCM)
#For motors
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)
GPIO.setup(ENA_B, GPIO.OUT)

PWM_A = GPIO.PWM(ENA_A, 100)
PWM_B = GPIO.PWM(ENA_B, 100)

PWM_A.start(100)
PWM_B.start(100)

def bgStart(func):
    thread = threading.Thread(target=func)
    thread.start()

def stop():
    PWM_B.ChangeDutyCycle(0)
    PWM_A.ChangeDutyCycle(0)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    
  
stop()



def move_forward():
    PWM_B.ChangeDutyCycle(95)
    PWM_A.ChangeDutyCycle(95)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
 

    
def reverse():
    PWM_B.ChangeDutyCycle(95)
    PWM_A.ChangeDutyCycle(95)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
   
def left_turn():
    PWM_B.ChangeDutyCycle(turningDSpeed)
    PWM_A.ChangeDutyCycle(turningLSpeed)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
   
def right_turn():
    PWM_B.ChangeDutyCycle(turningLSpeed)
    PWM_A.ChangeDutyCycle(turningDSpeed)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
  
    
#For Actuator
GPIO.setup(IN1A, GPIO.OUT)
GPIO.setup(IN2A, GPIO.OUT)
GPIO.setup(IN3A, GPIO.OUT)
GPIO.setup(IN4A, GPIO.OUT)   

step_sleep = 0.002
 
step_count = 3000

#For full step
GPIO.output( IN1A, GPIO.LOW )
GPIO.output( IN2A, GPIO.LOW )
GPIO.output( IN3A, GPIO.LOW )
GPIO.output( IN4A, GPIO.LOW )


def actuatorStop():
    GPIO.output(IN4A, GPIO.LOW)
    GPIO.output(IN3A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN1A, GPIO.LOW)
  

def actuatorDown():
    i = 0
     # Set the delay time for motor speed
    while i < step_count:
            if i % 4 == 0:
                GPIO.output(IN4A, GPIO.HIGH)
                GPIO.output(IN3A, GPIO.LOW)
                GPIO.output(IN2A, GPIO.LOW)
                GPIO.output(IN1A, GPIO.LOW)
            elif i % 4 == 1:
                GPIO.output(IN4A, GPIO.LOW)
                GPIO.output(IN3A, GPIO.LOW)
                GPIO.output(IN2A, GPIO.HIGH)
                GPIO.output(IN1A, GPIO.LOW)
            elif i % 4 == 2:
                GPIO.output(IN4A, GPIO.LOW)
                GPIO.output(IN3A, GPIO.HIGH)
                GPIO.output(IN2A, GPIO.LOW)
                GPIO.output(IN1A, GPIO.LOW)
            elif i % 4 == 3:
                GPIO.output(IN4A, GPIO.LOW)
                GPIO.output(IN3A, GPIO.LOW)
                GPIO.output(IN2A, GPIO.LOW)
                GPIO.output(IN1A, GPIO.HIGH)
        
            i += 1  # Increment step
            time.sleep(step_sleep)  # Delay for motor speed
    if i == step_count:
        actuatorStop()

def actuatorUp():
    d = 0
     # Set the delay time for motor speed
    while d < step_count:
            if d % 4 == 0:
                GPIO.output(IN4A, GPIO.LOW)
                GPIO.output(IN3A, GPIO.LOW)
                GPIO.output(IN2A, GPIO.LOW)
                GPIO.output(IN1A, GPIO.HIGH)
            elif d % 4 == 1:
                GPIO.output(IN4A, GPIO.LOW)
                GPIO.output(IN3A, GPIO.HIGH)
                GPIO.output(IN2A, GPIO.LOW)
                GPIO.output(IN1A, GPIO.LOW)
            elif d % 4 == 2:
                GPIO.output(IN4A, GPIO.LOW)
                GPIO.output(IN3A, GPIO.LOW)
                GPIO.output(IN2A, GPIO.HIGH)
                GPIO.output(IN1A, GPIO.LOW)
            elif d % 4 == 3:
                GPIO.output(IN4A, GPIO.HIGH)
                GPIO.output(IN3A, GPIO.LOW)
                GPIO.output(IN2A, GPIO.LOW)
                GPIO.output(IN1A, GPIO.LOW)
        
            d += 1  # Increment step
            time.sleep(step_sleep)  # Delay for motor speed
    if d == step_count:
        actuatorStop()
    
    

app = Flask(__name__)



@app.route('/', methods = [ 'POST', 'GET'])
def index():
    default_value = '0'
    if request.method == 'POST':
        back = request.form.get('forward', default_value)
        stopIn = request.form.get('stop', default_value)
        forward = request.form.get('back', default_value)
        right = request.form.get('right', default_value)
        left = request.form.get('left', default_value)
        
        down = request.form.get('down', default_value)
        #for motors
        if forward == '1':
            bgStart(move_forward)
            print('Moving forward')
        elif stopIn == '1':
            bgStart(stop)
            print('stopping ')
        elif back == '1':
            bgStart(reverse)
            print('Moving backward')
        elif left == '1':
            bgStart(left_turn)
            print('Moving left')   
        elif right == '1':
            bgStart(right_turn)
            print('Moving right')
         #for actuator
        elif down == '1':
            bgStart(actuatorDown)
            print('Moving down')
        else:
            bgStart(actuatorUp)
            print('Moving up')            
        return redirect('/')          
    return render_template('index.html')



@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sensor_data')
def sensor_data():
    def generate():
        while True:
            data = read_sensor_data()
            if data:
                yield f"data: {json.dumps(data)}\n\n"
            time.sleep(2)  # Stream data every 2 seconds

    return Response(generate(), mimetype='text/event-stream')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
