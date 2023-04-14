import cv2
import numpy as np

img = cv2.imread('starsno.jpg')
img_copy = img.copy()  # Make a copy of the original image
gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

stars = []
for i in range(1, num_labels):
    mask = (labels == i).astype(np.uint8)
    x, y = centroids[i]
    min_radius = 5  # or any other minimum value you choose
    r = int((stats[i, cv2.CC_STAT_WIDTH] + stats[i, cv2.CC_STAT_HEIGHT]) / 4)
    if r >= min_radius:
        x, y = centroids[i]
        b = cv2.mean(gray, cv2.UMat(mask))[0]
        stars.append((x, y, r, b))
        cv2.circle(img_copy, (int(x), int(y)), r + 5, (0, 255, 0), 2)
        print(r)

cv2.imwrite('detected_stars.jpg', img_copy)
cv2.imshow('Detected Stars', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()