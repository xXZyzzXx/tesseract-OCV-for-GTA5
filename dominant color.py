import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


def get_dominant_color(image, k=4):
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    clt = KMeans(n_clusters=k)
    labels = clt.fit_predict(image)

    label_counts = Counter(labels)

    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    return list(dominant_color)


bgr_image = cv2.imread('to_tess.png')
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
dom_color = get_dominant_color(hsv_image)
dom_color_hsv = np.full(bgr_image.shape, dom_color, dtype='uint8')
dom_color_bgr = cv2.cvtColor(dom_color_hsv, cv2.COLOR_HSV2BGR)
output_image = np.hstack((bgr_image, dom_color_bgr))
cv2.imshow('Dominant Color', dom_color_bgr)
cv2.waitKey(0)
