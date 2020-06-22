import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def tesseract(new_image):
    img = cv2.imread(new_image)
    text = pytesseract.image_to_string(img, lang='rus')
    print('Ваш текст: \n{}'.format(text))


def tess(new_image):
    image = cv2.imread(new_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    # cv2.imshow('sss', thresh)
    text = pytesseract.image_to_string(thresh, lang='rus', config='--psm 6')
    print('Второй вариант:', text, len(text))

    if len(text) > 10:
        score = text.split(' ')
        num = score[0][-1]
        num2 = score[1][0]
        bnum = False
        bnum2 = False
        finall = None
        d = [']', 'З']  # Базовый словарь
        d2 = [0, 3]
        print('Работаем с:', num, num2)

        flag = False
        try:
            num = int(num)
            bnum = True
            print('Это цифра, преобразование не требуется')
        except:  # Допилить перебор по словарю
            i = 0
            for o in d:
                if num == o:
                    num = d2[i]
                    print('Успешная итерация!', num, i)
                    flag = True
                    break
                else:
                    i += 1
            if not flag:
                print('В словаре не нашлось совпадений для ', num)
                num = None

        flag = False
        try:
            num2 = int(num2)
            bnum2 = True
            print('Это цифра, преобразование не требуется')
        except:  # Допилить перебор по словарю
            i = 0
            for o in d:
                if num2 == o:
                    num2 = d2[i]
                    print('Успешная итерация!', num2, i)
                    flag = True
                    break
                else:
                    i += 1
            if not flag:
                print('В словаре не нашлось совпадений для ', num2)
                num2 = None

        if num is not None and num2 is not None:  # Если оба найдены
            answer1 = num + 1
            answer2 = num2 - 1
            print('Два ответа: ', answer1, answer2)
            if answer1 == answer2:
                finall = answer1
            elif bnum == True and bnum2 == False:
                if num == 1:
                    finall = num2 - 1
                else:
                    finall = num + 1
            else:
                print('ошибка')

        elif num is not None or num2 is not None:  # Если один не нашёлся
            if num is not None:
                finall = num + 1
            elif num2 is not None:
                finall = num2 - 1
            else:
                print('Error')
        else:
            print('Оба варианта неверные')  # Можно добавить рандомный ответ на основании длинны списка

        print('Найдено! ', finall)

    elif len(text) == 10:
        score = text.split(' ')
        answer = 10 - len(score[1]) - 1
        print('Найдено:', answer)


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('\nПозиция: x = %d, y = %d' % (y, x))
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_pt = hsv_img[y, x]
        print('Цвет в HCV:', hsv_pt)  # вывод цвета
        hsv_min = (hsv_pt * 0.95).astype('uint8')
        hsv_max = (hsv_pt * 1.05).astype('uint8')
        result = cv2.inRange(hsv_img, hsv_min, hsv_max)
        # result = cv2.bitwise_not(result) # Реверс цвета
        new_image = 'new.png'
        cv2.imshow(new_image, result)
        cv2.imwrite(new_image, result)
        # tesseract(new_image)
        tess(new_image)
        cv2.waitKey(0)


image = 'thrash.png'
img = cv2.imread(image)
cv2.imshow("Output", img)
cv2.setMouseCallback('Output', onMouse)
cv2.waitKey(0)
