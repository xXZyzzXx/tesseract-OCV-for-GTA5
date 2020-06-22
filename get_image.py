import cv2


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
        print(max_frq, 'раз(а) встречается число', num)
        return num
    else:
        print('Все элементы уникальны')


image_file = "4.png"
img2 = cv2.imread(image_file)
x = 450
y = 300
h = 755
w = 1100
img = img2[y:y + h, x:x + w]  # Выделение рабочей области

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 420, 250)

contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
output = img.copy()

list_xy = []
maxlist = []
'''
    Тест для первой картинки:  h>54 and h<=57 and y>580 and y<585
    Тест для второй картинки:  h>=23 and h<=24 and y==450 or y==451
    Тест для третьей картинки:  h>41 and h<=44 and y>=170 and y<=171
    Тест для четвертой картинки:  h>=40 and h<=46 and y>=470 and y<=475
    Тест для пятой картинки:  h>=53 and h<=60 and y>=387 and y<=389
    '''
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    if 20 <= h <= 60:  # 2  h>=23 and h<=24 and y>=470 and y<=475
        maxlist.append(h)
        list_xy.append(y)

list_xy.sort()
maxlist.sort()
final_list = zip(list_xy, maxlist)
final_list = list(final_list)
num_max = lets_go(list_xy)
num_max2 = lets_go(maxlist)
razbros = 4
list_counters = []
list_counters2 = []

for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    if num_max2 - razbros <= h <= num_max2 + razbros and num_max - razbros <= y <= num_max + razbros:  # Рабочая область
        list_counters.append((x, y))
        list_counters2.append((x + w, y + h))
        cv2.rectangle(output, (x, y), (x + w, y + h), (255, 255, 255), 2)

list_counters.sort()
list_counters2.sort()
cv2.rectangle(output, list_counters[0], list_counters2[-1], (255, 105, 105), 1)
coords = list_counters[0]
coords2 = list_counters2[-1]

img5 = img[coords[1]:coords2[1], coords[0]:coords2[0]]

cv2.imshow("icon", img5)
cv2.imshow("thrash", output)
cv2.imwrite("thrash.png", img5)
cv2.waitKey(0)
