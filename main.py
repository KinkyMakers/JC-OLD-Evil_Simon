# Shocking Simon
#
#
# Lot of stuff taken from the original example game for this device:
#
# Game play based on information provided here:
# http://www.waitingforfriday.com/?p=586
#
# Author: Carter Nelson
# MIT License (https://opensource.org/licenses/MIT)

from adafruit_circuitplayground.express import cpx
from digitalio import DigitalInOut, Direction, Pull
import time
import random
import board
import touchio

# Boot to lights on to show ready
cpx.pixels.fill(0x100010)
level = 0
shock = 1
mode = "setup"
waitforinput = False
currentpos = 0
guess_timeout = 3.0
shocking = False

touch1 = DigitalInOut(board.A6)
touch2 = DigitalInOut(board.A7)
touch3 = DigitalInOut(board.A1)
touch4 = DigitalInOut(board.A3)

touch1.direction = Direction.INPUT
touch2.direction = Direction.INPUT
touch3.direction = Direction.INPUT
touch4.direction = Direction.INPUT

touch1.pull = Pull.UP
touch2.pull = Pull.UP
touch3.pull = Pull.UP
touch4.pull = Pull.UP


toy = DigitalInOut(board.A2)
toy.direction = Direction.OUTPUT
toy.value = False

#Wake up Pet
for t in range(100,2000,50):
    cpx.start_tone(t)
    time.sleep(.05)
    
cpx.stop_tone()



difficulty = {
    0 : 4,
    1 : 6,
    2 : 8,
    3 : 4,
    4 : 6,
    }
pixelgroup = {
    1 : { 'pixels':(0,1,2) },
    2 : { 'pixels':(2,3,4) },
    3 : { 'pixels':(5,6,7) },
    4 : { 'pixels':(7,8,9) },
   }
pixelcolour = {
    1 : { 'colour':0x001100 },
    2 : { 'colour':0x111100 },
    3 : { 'colour':0x000011 },
    4 : { 'colour':0x110000 },
   }

def makesequence(level):

    level = level % 5 #game continues in a cyclical manner - levels increase, as pet progresses reward time increases with each level, but so does the punishment
    upperbounds = difficulty[level] #sets up the number of steps in the range
    gamesequence = [random.randint(1,4) for g in range(int(upperbounds))]
    
    return gamesequence
    
    
def indicaterandom(inputseq, step):
    for i in range(0,step):
        print (inputseq[i])
        cpx.pixels.fill(0x000000)
        time.sleep (.5)
        
        pixelstolight = pixelgroup[random.randint(1,4)]
        
        for p in pixelstolight['pixels']:
            cpx.pixels[p] = pixelcolour[inputseq[i]]['colour']
            
        time.sleep(2)
        
def indicatenormal(inputseq,step):
    for i in range(0,step):
        print (inputseq[i])
        cpx.pixels.fill(0x000000)
        time.sleep (.5)

        for p in pixelgroup[inputseq[i]]['pixels']:
            cpx.pixels[p] = pixelcolour[inputseq[i]]['colour']
            
        time.sleep(2)

def petdoesntcum(level):
    for t in range(100, 1000, 10):
        cpx.start_tone(t)
        time.sleep(.05)
        
    for t in range(20):
        cpx.start_tone(500)
        time.sleep(.5)
        cpx.stop_tone()
    cpx.start_tone(300)
    return
    
def makepetcum(level):
    sleepytime = 1
    if level == "one":
        rangetocum = 1
    elif level >= 0:
        rangetocum = 10 * ( level + 1)
        
    for t in range(rangetocum):
        
        if level != "one":
            cpx.pixels.fill(0x000000)
            currentpixel = t % 10 # current step modulo (remainder of divide) by 10 - 1 number for each pixel will drop out hopefully
            print(currentpixel)
            cpx.pixels[currentpixel] = (0x100010)
        
        toy.value = True
        print("Pet gets the D")
        if sleepytime >= .5:
            sleepytime = sleepytime - .05
        elif sleepytime < .5:
            sleepytime = .5
            
        time.sleep(sleepytime)
        toy.value = False
        print("Pet looses the D")
        time.sleep(sleepytime)
		
        
def checkbuttons():
    button = False
    if touch1.value == False:
        button = 1
    if touch2.value == False:
        button = 2        
    if touch3.value == False:
        button = 3    
    if touch4.value == False:
        button = 4
        
    return button
        
        
while True:
    #makepetcum(100)  #this is just for testing - it will run the toy for a 100 level cycle
    level_button = cpx.button_a
    shock_button = cpx.button_b
    
    if mode == "setup":
        if level_button and shock_button: #sets mode to game time
            mode = "gametime"
            print("Oh Noes! Game Time")
            
            gamesequence = makesequence(level)
            step = 0
            playing = 0
            
            
        elif level_button: #sets difficulty level
            if level <4:
                level = level +1
            elif level == 4:
                level = 0
            print("Level: " + str(level))
            
        elif shock_button: #sets shock level
            if shock <5:
                shock = shock +1
            elif shock == 5:
                shock = 1
            print("Shock: "+str(shock))

        for l in range(0,5):
            if l <=level:
                cpx.pixels[l] = 0x100000
            elif l > level:
                cpx.pixels[l] = 0x050005
            
            
        for s in range(9,4,-1):
            if s > 9 - int(shock):
                cpx.pixels[s] = 0x001010
            else:
                cpx.pixels[s] = 0x050005
        

                
    if mode == "gametime" and waitforinput == False:
        print (gamesequence)
        cpx.pixels.fill(0x000000)
        if step == len(gamesequence):
            print("YOU WIN!!!!!")
            makepetcum(level)
            level += 1
            gamesequence = makesequence(level)
            step=0
            playing = 0
            time.sleep(4)
            
        elif step < len(gamesequence):
            makepetcum("one")
            if (level % 4)  > 2:
                indicaterandom(gamesequence,step+1)
                    
            elif (level % 4) <= 2:
                indicatenormal(gamesequence,step+1)

            
            waitforinput = True
            cpx.pixels.fill(0x020202)
            playing = 0
        
    
    if mode == "gametime" and waitforinput == True:
        
        print("cum on now, give Sir an answer")
        guess_start_time = time.monotonic()

        while playing <= step and waitforinput == True:
            button_input = checkbuttons()
            
            print(str(playing) + " : " + str(step) + " / " +str(button_input) + " : " + str(gamesequence[playing]))
        

            if button_input != False and button_input == gamesequence[playing]:
                cpx.pixels.fill(0x000000)
                print("Pet did good!")
                playing  = playing + 1
                cpx.stop_tone()
                cpx.play_tone(300,.1)
                for ty in range (3):
                    toy.value = True
                    time.sleep(.3)
                    toy.value = False
                guess_start_time = time.monotonic()
                cpx.pixels.fill(0x020202)
                
                
            elif button_input != False:
                print("Buzzzzzz - wrong button!")
                playing = 0
                step = 0
                waitforinput = False
                petdoesntcum(level)
                
            if time.monotonic() > guess_start_time + guess_timeout:
                cpx.start_tone (400)
                
            if playing > step:
                waitforinput = False
                step += 1
                print("Completed this round")
                
            time.sleep(.01)
            print("end fo while loop")
        

    #Debounce a little
    time.sleep(.05)
    
