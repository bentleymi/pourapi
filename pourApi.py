from flask import Flask
from flask import request as R
import RPi.GPIO as GPIO
from time import sleep
import threading, logging

app = Flask(__name__)

@app.route('/pourApi')
def pourApi():
    T1,T2,T3,T4,T5,T6=float(R.args.get('M1')),float(R.args.get('M2')),float(R.args.get('M3')),float(R.args.get('M4')),float(R.args.get('M5')),float(R.args.get('M6'))
    logging.info("pour request, mod1=%s, mod2=%s, mod3=%s, mod4=%s, mod5=%s, mod6=%s",T1,T2,T3,T4,T5,T6)
    makeDrink(T1,T2,T3,T4,T5,T6)
    message = "Hello, you asked for %s of #1, %s of #2, %s of #3, %s of #4, %s of #5, %s of #6" % (T1,T2,T3,T4,T5,T6)
    logging.info("pour complete") 
    return message

@app.route('/')
def mainPage():
    message='''
    <html><body>
    <form action="/pourApi" method="get">
    KnobCreek: <input type="number" min="0" step="0.1" name="M1"><br><br>
    1800: <input type="number" min="0" step="0.1" name="M2"><br><br>
    SeagramsLime: <input type="number" min="0" step="0.1" name="M3"><br><br>
    MargarittaMix: <input type="number" min="0" step="0.1" name="M4"><br><br>
    CranApple: <input type="number" min="0" step="0.1" name="M5"><br><br>
    Coke: <input type="number" min="0" step="0.1" name="M6"><br><br>
    <input type="submit" value="Submit">
    </form>
    </body></html>
    '''
    return message

@app.route('/recipes')
def drinkPage():
    message='''
    <html><body>
    <form action="/pourApi" method="get">
    <input type="hidden" min="0" value="15" name="M1">
    <input type="hidden" min="0" value="15" name="M2">
    <input type="hidden" min="0" value="15" name="M3">
    <input type="hidden" min="0" value="0" name="M4">
    <input type="hidden" min="0" value="0" name="M5">
    <input type="hidden" min="0" value="0" name="M6">
    <input type="submit" value='Negroni'>
    </form>
    <br>
    <form action="/pourApi" method="get">
    <input type="hidden" min="0" value="0" name="M1">
    <input type="hidden" min="0" value="15" name="M2">
    <input type="hidden" min="0" value="15" name="M3">
    <input type="hidden" min="0" value="0" name="M4">
    <input type="hidden" min="0" value="0" name="M5">
    <input type="hidden" min="0" value="15" name="M6">
    <input type="submit" value='Boulavardier'>
    </form>
    <br>
    <form action="/pourApi" method="get">
    <input type="hidden" min="0" value="0" name="M1">
    <input type="hidden" min="0" value="0" name="M2">
    <input type="hidden" min="0" value="0" name="M3">
    <input type="hidden" min="0" value="2" name="M4">
    <input type="hidden" min="0" value="2" name="M5">
    <input type="hidden" min="0" value="30" name="M6">
    <input type="submit" value='Old Fashioned'>
    </form>
    </body></html>
    '''
    return message

def spinIt(GPIO,t):
    pin=6
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    sleep(t)
    GPIO.output(pin,GPIO.HIGH)

def mixIt(GPIO,revolutions):
    step1=17
    step2=27
    step3=22
    step4=23
    GPIO.setup(step1,GPIO.OUT)
    GPIO.setup(step2,GPIO.OUT)
    GPIO.setup(step3,GPIO.OUT)
    GPIO.setup(step4,GPIO.OUT)
    count = 0
    print("Will stir for " + str(revolutions) + " revolutions.")
    if revolutions <= 10:    
        revolutions = revolutions * 500
    else:
        revolutions = 5000
    while count < revolutions:
        GPIO.output(step1,GPIO.HIGH)    
        GPIO.output(step2,GPIO.LOW)
        GPIO.output(step3,GPIO.LOW)
        GPIO.output(step4,GPIO.LOW)
        sleep(0.0025)
        GPIO.output(step1,GPIO.LOW)    
        GPIO.output(step2,GPIO.HIGH)
        GPIO.output(step3,GPIO.LOW)
        GPIO.output(step4,GPIO.LOW)
        sleep(0.0025)
        GPIO.output(step1,GPIO.LOW)    
        GPIO.output(step2,GPIO.LOW)
        GPIO.output(step3,GPIO.HIGH)
        GPIO.output(step4,GPIO.LOW)
        sleep(0.0025)
        GPIO.output(step1,GPIO.LOW)    
        GPIO.output(step2,GPIO.LOW)
        GPIO.output(step3,GPIO.LOW)
        GPIO.output(step4,GPIO.HIGH)
        sleep(0.0025)
        count=count+1
    GPIO.cleanup()

        
def pourIt(GPIO,pin,T):
    print("pin:"+str(pin)+" time:"+str(T)+"\n")
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    sleep(T)
    GPIO.output(pin,GPIO.HIGH)
    
def makeDrink(T1,T2,T3,T4,T5,T6):
    GPIO.setmode(GPIO.BCM)
    motor1=26
    motor2=16
    motor3=13
    motor4=12
    motor5=20
    motor6=21
    x=threading.Thread(target=pourIt, args=(GPIO,motor1,T1))
    y=threading.Thread(target=pourIt, args=(GPIO,motor2,T2))
    z=threading.Thread(target=pourIt, args=(GPIO,motor3,T3))
    xz=threading.Thread(target=pourIt, args=(GPIO,motor4,T4))
    yz=threading.Thread(target=pourIt, args=(GPIO,motor5,T5))
    zz=threading.Thread(target=pourIt, args=(GPIO,motor6,T6))
    x.start()
    y.start()
    z.start()
    xz.start()
    yz.start()
    zz.start()
    #need to sleep 1 more second than the request
    setA=set([T1,T2,T3,T4,T5,T6])
    t = max(setA)
    sleep(1)
    a=threading.Thread(target=mixIt, args=(GPIO,t))
    b=threading.Thread(target=spinIt, args=(GPIO,t))
    a.start()
    b.start()
    sleep(t+1)
    GPIO.cleanup()

#configure logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO)

#flask execution
app.run(host='192.168.200.142',threaded=True)
GPIO.cleanup()
