import cv2
import pytesseract
import numpy as np
import random
from time import time
import movement_in_game

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
path = r'C:\Users\offic\Desktop\OCR\screens'
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
k0 = 0x30
k1 = 0x31
k2 = 0x32
k3 = 0x33
k4 = 0x34
k5 = 0x35
k6 = 0x36
k7 = 0x37
k8 = 0x38
k9 = 0x39
list_k = [k0, k1, k2, k3, k4, k5, k6, k7, k8, k9]


def lets_go(arr):  # Выводит значение наиболее частого числа
    N = len(arr)
    num = arr[0]
    max_frq = 1
    for i in range(N - 1):
        frq = 1
        for k in range(i + 1, N):
            if arr[i] == arr[k]:
                frq += 1
        if frq > max_frq:
            max_frq = frq
            num = arr[i]

    if max_frq > 1:
        # print(max_frq, 'раз(а) встречается число', num)
        return num
    else:
        pass
        # print('Все элементы уникальны')


def lets_go2(arr):  # Выводит значение наиболее частого числа
    N = len(arr)
    num = arr[0]
    max_frq = 1
    for i in range(N - 1):
        frq = 1
        for k in range(i + 1, N):
            if str(arr[i]) == str(arr[k]):
                frq += 1
        if frq > max_frq:
            max_frq = frq
            num = arr[i]

    if max_frq > 1:
        # print(max_frq, 'раз(а) встречается число', num)
        return num, arr.index(num)
    else:
        pass
        # print('Все элементы уникальны')


def get_srez(image_file):  # Получить картинку по контурам для обработки
    img2 = cv2.imread(image_file)
    x = 450  # 185#450
    y = 300  # 185#300
    h = 755  # 750#755
    w = 1100  # 950#1100
    img = img2[y:y + h, x:x + w]  # Выделение рабочей области
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 420, 250)  # Отфильтровать 420, 250
    cv2.imshow('2', edged)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    output = img.copy()
    # cv2.imwrite(path + '\window%ds.png' % random.randrange(1000), edged)
    list_xy = []  # Список координаты y
    maxlist = []  # Список высоты
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if 20 <= h <= 60:  # 2  h>=23 and h<=24 and y>=470 and y<=475
            maxlist.append(h)
            list_xy.append(y)
    list_xy.sort()
    maxlist.sort()
    num_max = lets_go(list_xy)
    num_max2 = lets_go(maxlist)
    razbros = 4
    list_counters = []
    list_counters2 = []
    list_wh = []

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if num_max2 - razbros <= h <= num_max2 + razbros and num_max - razbros <= y <= num_max + razbros:  # Рабочая область
            list_counters.append((x, y))
            list_counters2.append((x + w, y + h))
            list_wh.append((w, h))
            # cv2.rectangle(output, (x, y), (x + w, y + h), (255, 255, 255), 5)

    hsv_img = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
    hsv_colors = []
    list_colors = []
    for h in range(len(list_wh)):
        new_wh = int(list_wh[h][0])
        new_wh2 = int(list_wh[h][1])

        cv2.rectangle(output, (int(list_counters[h][0]) + new_wh // 2, int(list_counters[h][1])),
                      (int(list_counters[h][0]) + new_wh // 2, int(list_counters[h][1]) + new_wh2), (105, 255, 105), 1)

        cv2.rectangle(output, (int(list_counters[h][0]), int(list_counters[h][1]) + new_wh2 // 2),
                      (int(list_counters[h][0]) + new_wh, int(list_counters[h][1]) + new_wh2 // 2), (105, 255, 105), 1)

        cv2.line(output, (int(list_counters[h][0]) + new_wh // 2, int(list_counters2[h][1]) - new_wh2 // 2),
                 (int(list_counters[h][0]) + new_wh // 2, int(list_counters2[h][1]) - new_wh2 // 2), (255, 0, 0), 3)

        hsv_pt = hsv_img[int(list_counters2[h][1]) - new_wh2 // 2, int(list_counters[h][0]) + new_wh // 2]
        hsv_colors.append(hsv_pt)

    for t in hsv_colors:  # Вроде как второй список уже не нужен, в lets_go оно само в str преобразовывает
        list_colors.append(str(t))

    fuck = lets_go2(list_colors)

    point = hsv_colors[fuck[1]]  # Доступ к индексу второго списка
    list_counters.sort()
    list_counters2.sort()
    coords = list_counters[0]
    coords2 = list_counters2[-1]
    img5 = img[coords[1]:coords2[1], coords[0]:coords2[0]]
    # cv2.imshow("icon", output)
    # cv2.imwrite("to_tess.png", img5)
    find_hsv(point, img5)


def find_hsv(hsv_pt, img):
    name_img = 'result.png'
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = (hsv_pt * 0.95).astype('uint8')
    hsv_max = (hsv_pt * 1.05).astype('uint8')
    result = cv2.inRange(hsv_img, hsv_min, hsv_max)
    cv2.imwrite(name_img, result)
    tess(name_img)


def tess(new_image):
    image = cv2.imread(new_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    text = pytesseract.image_to_string(thresh, lang='rus', config='--psm 6')
    # print('Результат тессеракта:', text, '\n..КОНЕЦ..')
    print(text)

    if len(text) > 10:
        score = text.split(' ')
        num = score[0][-1]
        num2 = score[1][0]
        bnum = False
        bnum2 = False
        finall = None
        d = [']', 'З']
        d2 = [0, 3]
        # print('Работаем с:', num, num2)

        flag = False
        try:
            num = int(num)
            bnum = True
            # print('Это цифра, преобразование не требуется')
        except:  # Допилить перебор по словарю
            i = 0
            for o in d:
                if num == o:
                    num = d2[i]
                    # print('Успешная итерация!', num, i)
                    flag = True
                    break
                else:
                    i += 1
            if not flag:
                # print('В словаре не нашлось совпадений для ', num)
                num = None

        flag = False
        try:
            num2 = int(num2)
            bnum2 = True
            # print('Это цифра, преобразование не требуется')
        except:  # Допилить перебор по словарю
            i = 0
            for o in d:
                if num2 == o:
                    num2 = d2[i]
                    # print('Успешная итерация!', num2, i)
                    flag = True
                    break
                else:
                    i += 1
            if not flag:
                # print('В словаре не нашлось совпадений для ', num2)
                num2 = None

        if num is not None and num2 is not None:  # Если оба найдены
            answer1 = num + 1
            answer2 = num2 - 1
            # print('Два ответа: ', answer1, answer2)
            if answer1 == answer2:
                finall = answer1
            elif bnum == True and bnum2 == False:
                if num == 1:
                    finall = num2 - 1
                else:
                    finall = num + 1
            else:
                print('Error')

        elif num is not None or num2 is not None:  # Если один не нашёлся
            if num is not None:
                finall = num + 1
            elif num2 is not None:
                finall = num2 - 1
            else:
                print('Error')
        else:
            print('Оба варианта неправильные')  # Можно добавить рандомный ответ на основании длинны списка

        if finall is not None:
            print('Найдено! ', finall)
            movement_in_game.press(list_k[finall])
            print('Должно нажать')

    elif len(text) == 10:
        score = text.split(' ')
        answer = 10 - len(score[1]) - 1
        print('Найдено:', answer)
        movement_in_game.press(list_k[answer])
        print('Должно нажать')


image = '3.png'
get_srez(image)
