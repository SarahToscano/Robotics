import numpy as np
import cv2

# sasq = np.random.randint(100, size=(5, 1))
# narut = np.random.randint(100, size=(5, 1))
# amor = np.hstack((sasq, narut))
# print(sasq)
# print(narut)
# print(amor)

# Draw a diagonal blue line of thickness of 5 pixels
image = np.zeros((512, 512, 3), np.uint8)  # black canvas
cv2.line(image, (0, 0), (511, 511), (255, 127, 0), 5)
cv2.imshow("Blue Line", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

i = 1
while True:
    print('aaaaa')
    i = i+1
    if(i > 22):
        break
