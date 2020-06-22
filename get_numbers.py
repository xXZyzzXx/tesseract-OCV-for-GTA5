import cv2
import pytesseract


def tesseract(new_image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    img = cv2.imread(new_image)
    text = pytesseract.image_to_string(img, lang='rus')
    print('Ваш текст: \n{}'.format(text))


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('\nПозиция: x = %d, y = %d' % (y, x))

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_pt = hsv_img[y, x]
        print('Цвет в HCV: '.format(hsv_pt))  # вывод цвета
        hsv_min = (hsv_pt * 0.95).astype('uint8')
        hsv_max = (hsv_pt * 1.05).astype('uint8')
        result = cv2.inRange(hsv_img, hsv_min, hsv_max)
        #result = cv2.bitwise_not(result) # Реверс цвета
        new_image = 'new.png'
        cv2.imshow(new_image, result)
        cv2.imwrite(new_image, result)
        tesseract(new_image)
        cv2.waitKey(0)


image = 't3.png'
img = cv2.imread(image)
cv2.imshow("Output", img)
cv2.setMouseCallback('Output', onMouse)
cv2.waitKey(0)