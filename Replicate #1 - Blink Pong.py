#Blink Pong#
#By Youssef Kusibati inspired by Edge Impulse#

#Importing Modules and Packages

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from tkinter import *
import tkinter as tk
import time
import random
import threading    

#Global Variables

global isFailed

blinks = 0                                                      
blinked = False                                               

IP = "0.0.0.0"                                                 
PORT = 5000                                                   

#Functions

#Handling blink from Mind Monitor

def blink_handler(address, *args):
    global blinks, blinked

    blinks += 1
    blinked = True
    print("Blink detected ")

#Communicating with Muse 

def get_dispatcher():
    dispatcher = Dispatcher()
    dispatcher.map("/muse/elements/blink", blink_handler)
    
    return dispatcher

def start_blocking_server(ip, port):
    server = BlockingOSCUDPServer((ip, port), dispatcher)
    server.serve_forever()  

def dispatch():
    global dispatcher

    dispatcher = get_dispatcher()
    start_blocking_server(IP, PORT)


#Game

#Moving the paddle

def movepaddleLR(paddle, dir, x, y = 0):
    x1, y1, x2, y2 = c.coords(paddle)                               
    if ((x1 > 0 and dir == 'l') 
            or (x2 < 400 and dir == 'r')):                          
        c.move(paddle, x, y)
        c.update()
    elif dir == 'stop':                                             
        c.move(paddle, 0, 0)
        c.update()


#Ball Movement

def move_ball(ball, sp, score):
    global wait, blink_window_wait, blinked

    s = random.randint(-sp, sp)                                   
    x, y = s, 0-sp                                                  
    c.move(ball, x, y)

    for p in range(1, 500000):                                      
        l, t, r, b = c.coords(ball)                               
        txtS.delete(0, END)                                         
        txtS.insert(0, "Score: " + str(score))                      

        if(r >= 400 and x >= 0 and y < 0): 
            x, y = 0-sp, 0-sp
        elif(r >= 400 and x >= 0 and y >= 0): 
            x, y = 0-sp, sp
        elif(l <= 0 and x < 0 and y < 0): 
            x, y = sp, 0-sp
        elif(l <= 0 and x < 0 and y >= 0):
            x, y = sp, sp
        elif(t <= 0 and x >= 0 and y < 0): 
            x, y = sp, sp
        elif(t <= 0 and x < 0 and y < 0): 
            x, y = 0-sp, sp
        elif(b >= 385):                                            
            tchPt = l + 10                                      
            bsl, bst, bsr, bsb = c.coords(paddle)
            if(tchPt >= bsl and tchPt <= bsr):                     
                n = random.randint(-sp, sp)
                x, y = n, 0-sp
                score += 1
                  
            else:                                                  
                global isFailed
                isFailed = True
                break                                           
        
        time.sleep(.025)                                            

        if blinked == True:                                         
            c.itemconfigure(blink_window, state='normal')           
            blinked = False

        if blink_window_wait == 50:                              
            blink_window_wait = 0
            c.itemconfigure(blink_window, state='hidden')           
        else:
            blink_window_wait += 1

        what = blinks % 4                                           
        if what == 1:                                               
            movepaddleLR(paddle, 'l', 0-paddle_speed)              
        elif what == 0 or what == 2:
            movepaddleLR(paddle, 'stop', 0)                         
        elif what == 3:
            movepaddleLR(paddle, 'r', paddle_speed)                 

        c.move(ball, x, y)
        c.update()

#Initializing all variable and starting the game

def pong():
    global c, ball, txtS, paddle, blink_window, ball_speed, paddle_speed
    global score, wait, blink_window_wait

  
    root = Tk()
    root.minsize(400,400)
    root.title("Blink Pong")
    paddle_speed = 5
    ball_speed = 5
    score = 6
    wait = 0
    blink_window_wait = 0
    global isFailed
    isFailed = False

    # Muse Communication
    thread = threading.Thread(target=dispatch)
    thread.daemon = True
    thread.start()

    #Creating the Canvas
    c = Canvas(width=400, height=400, background='#006cff')
    c.pack()
    paddle = c.create_rectangle(150, 385, 250, 400, fill='red', outline='red')   
    ball = c.create_oval(190, 365, 210, 385, fill='orange', outline='red')             
    txtS = tk.Entry(c, text='0')                                                   
    txtScore = c.create_window(300, 0, anchor='nw', window=txtS)

    # Blink Detection Label
    blink_label = tk.Label(c, text='Blink detected')
    blink_window = c.create_window(10, 10, anchor='nw', window=blink_label)
    c.itemconfigure(blink_window, state='hidden')
    
    #Moving the paddle using the keyboard
    root.bind("<KeyPress-Left>", lambda event: movepaddleLR(paddle, 'l', 0-paddle_speed))
    root.bind("<KeyPress-Right>", lambda event: movepaddleLR(paddle, 'r', paddle_speed))
    
    # Main loop and if score hits zero the game terminates + a small time count-down.
    while 1:
        move_ball(ball, ball_speed, score)                                       
        score -= 1 
                                                                    
        if score <= 0:
            exit(1)
    root.mainloop()

#Starting the game

if __name__ == "__main__":
    pong()                                                                         
    
