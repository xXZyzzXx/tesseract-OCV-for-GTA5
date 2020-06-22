import numpy as np
from PIL import ImageGrab
import cv2
import time
import random
import together
import movement_in_game

path = r'C:\Users\offic\Desktop\OCR\screens'
A = 0x41


def main():
    last_time = time.time()
    i = 0
    while True:
        screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
        # print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        # cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        cv2.imwrite('window.png', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        # movement_in_game.press(A)
        '''
        try:
            together.get_srez('window.png')  # Запускает обработку изображения 
        except:
            pass
        '''
        # cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


main()
