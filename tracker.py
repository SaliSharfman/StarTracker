import os
import cv2
import numpy as np

dir_src = 'images'
dir_dest = 'detected_stars'
filename = 'stars2.JPG'
path = os.path.join(os.getcwd(), dir_dest)
try:
    os.mkdir(path)
except:
    pass
img = cv2.imread(f'{dir_src}\{filename}')
img_copy = img.copy()  # Make a copy of the original image
gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blur, 5, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow('Detected Stars', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

stars = []
for i in range(1, num_labels):
    mask = (labels == i).astype(np.uint8)
    x, y = centroids[i]
    min_radius = 2  # or any other minimum value you choose
    r = int((stats[i, cv2.CC_STAT_WIDTH] + stats[i, cv2.CC_STAT_HEIGHT]) / 4)
    if r >= min_radius:
        x, y = centroids[i]
        b = cv2.mean(gray, cv2.UMat(mask))[0]
        stars.append((x, y, r, b))
        cv2.circle(img_copy, (int(x), int(y)), r + 5, (0, 255, 0), 2)
        print(r)

cv2.imwrite(f'{dir_dest}\detected_{filename}', img_copy)
cv2.imshow('Detected Stars', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
