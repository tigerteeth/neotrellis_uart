import busio
import board
import time
import adafruit_trellism4

BAUDRATE = 9600

trellis = adafruit_trellism4.TrellisM4Express()

# Define the NeoPixel color values for pressed and unpressed buttons
COLOR_PRESSED = (0, 255, 50)     # Green
COLOR_UNPRESSED = (0, 0, 0)     # Off (Black)

# Initialize the button states
button_states = [[False] * 4 for _ in range(8)]

trellis.pixels[(0, 0)] = COLOR_PRESSED

held = False

while True:
    pressed = trellis.pressed_keys
    if pressed:
        if held == False:
            held = True
            button = pressed[0]
            #print("Pressed: ", button)        
            # Update the button states and LED colors
            for row in range(8):
                for col in range(4):
                    if (row, col) == button:
                        button_states[row][col] = True
                        trellis.pixels[(row, col)] = COLOR_PRESSED
                    else:
                        button_states[row][col] = False
                        trellis.pixels[(row, col)] = COLOR_UNPRESSED
            
            with busio.UART(board.SDA, board.SCL, baudrate=BAUDRATE) as uart:
                coor = str(pressed[0][0])+str(pressed[0][1])+str(' \n')
                print(coor)
                data = bytearray(coor, 'utf-8')
                uart.write(data)
    else:
        held = False
        
    
