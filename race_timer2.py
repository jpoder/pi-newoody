#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO  
import time
from time import sleep
GPIO.setmode(GPIO.BCM)  

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #lane 1
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #lane 2
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #lane 3
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #lane 4
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #starting line
  
  
def start_callback(channel):  
    #print "rising edge detected on 17:  START"  
    global start_time 
    global race_started
    start_time = time.time()
    print "start"
    race_started = True
  
def lane1_callback(channel):  
    #print "rising edge detected on 22: Lane 1 finish"  
    global lane1_time 
    global start_time
    global lane1_finish
    lane1_time = time.time() - start_time
    print "lane 1 finish"
    #print lane1_time
    lane1_finish = True

def lane2_callback(channel):
    #print "rising edge detected on 23: Lane 2 finish"
    global lane2_time 
    global start_time
    global lane2_finish
    lane2_time = time.time() - start_time
    print "lane 2 finish"
    lane2_finish = True

def lane3_callback(channel):
    #print "rising edge detected on 24: Lane 3 finish"
    global lane3_time 
    global start_time
    global lane3_finish
    lane3_time = time.time() - start_time
    print "lane 3 finish"
    lane3_finish = True

def lane4_callback(channel):
    #print "rising edge detected on 25: Lane 3 finish"
    global lane4_time
    global start_time
    global lane4_finish
    lane4_time = time.time() - start_time
    print "lane 4 finish"
    lane4_finish = True

def main():  

    global start_time
    global lane1_time
    global lane2_time
    global lane3_time
    global lane4_time
    global race_started
    global lane1_finish
    global lane2_finish
    global lane3_finish
    global lane4_finish

    #raw_input("Press Enter when ready to race\n>")  
    #start_time = 0 #time.time() #this is the time when the timer starts  
    race_started = False  
    lane1_finish = False
    lane2_finish = False
    lane3_finish = False
    lane4_finish = False

    GPIO.add_event_detect(17, GPIO.RISING, callback=start_callback, bouncetime=800)  

    GPIO.add_event_detect(22, GPIO.RISING, callback=lane1_callback, bouncetime=600)  
    GPIO.add_event_detect(23, GPIO.RISING, callback=lane2_callback, bouncetime=600)  
    GPIO.add_event_detect(24, GPIO.RISING, callback=lane3_callback, bouncetime=600)  
    GPIO.add_event_detect(25, GPIO.RISING, callback=lane4_callback, bouncetime=600)
    while (race_started == False): 
        #wait here for the starting line to drop
        sleep(0.01)
    print "race started!"
    while (lane1_finish == False or lane2_finish == False or lane3_finish == False or lane4_finish == False) and ((time.time() - start_time) < 7):
        sleep(0.01) #wait for all lanes to finish or timeout
    print "race finished"

    if lane1_finish == False:
        lane1_time = 99
    if lane2_finish == False:
        lane2_time = 99
    if lane3_finish == False:
        lane3_time = 99
    if lane4_finish == False:
        lane4_time = 99

    print "lane 1 ", lane1_time
    print "lane 2 ", lane2_time
    print "lane 3 ", lane3_time
    print "lane 4 ", lane4_time
  
    GPIO.cleanup()           # clean up GPIO on normal exit  

    return (lane1_time,lane2_time,lane3_time, lane4_time)

if __name__ == "__main__":
    main()
