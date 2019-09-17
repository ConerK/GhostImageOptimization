import cv2
import numpy as np

# mobile inch
inch = 5.1
# mobile pixel
# mobile_width = 800
# mobile_height = 450
# samsung 5.1inch 1440*2560
mobile_width = 2560
mobile_height = 1440
# Index of refraction for windshield glass
n = 1.518
# Angle between windshield and input display
Beta = 65
# Luminance ratio between two virtual images
sita = 1.8
# Thickness of windshield
d = 4.5
# pixel size  1 inch = 25.4mm  samsung 5.1in  129.54mm  1440*2560
ps = inch * 25.4 / np.sqrt(np.square(mobile_height) + np.square(mobile_width))
print("ps: {}".format(ps))

# 这里计算两个虚拟成像的偏移距离有误差，可以参考另一篇论文，但是不能用到这里去除重影，效果不对
# 1× sin �= n∙ sin �
sinB = np.sin(Beta * np.pi / 180) / n
# z= 根号2d tan �
z = np.sqrt(2) * d * (sinB / np.sqrt(1 - np.square(sinB)))
print("z: {}".format(z))
# m = z / pixel size
m = z / ps
m = int(round(m))
print("m: {}".format(m))


img_path = 'hud.png'
img = cv2.imread(img_path)
rgb = cv2.resize(img, (mobile_width, mobile_height))
# 这里改变shiftMatrix的行和列与图片做矩阵乘法，手机的尺寸实际值很重要，会影响实际结果
for i in range(200):
    if mobile_width * mobile_height % m == 0:
        print(m)
        break
    m += 1
# shift matrix
shiftMatrix = np.eye(m, k=1)
for i in range(m):
    for j in range(m):
        if j == i:
            shiftMatrix[i][j] = 1
            break

I = np.identity(m)
W = I + sita * shiftMatrix
# 最小二乘法规则，可参考https://blog.csdn.net/bitcarmanlee/article/details/51589143
WHat = np.linalg.inv(W.T.dot(W)).dot(W.T)
rgb_r = np.reshape(rgb[:, :, 0], (m, -1))
rgb_g = np.reshape(rgb[:, :, 1], (m, -1))
rgb_b = np.reshape(rgb[:, :, 2], (m, -1))
rgbR = WHat.dot(rgb_r).clip(0, 255)
rgbG = WHat.dot(rgb_g).clip(0, 255)
rgbB = WHat.dot(rgb_b).clip(0, 255)
rgbR = np.reshape(rgbR, (-1, mobile_width))
rgbG = np.reshape(rgbG, (-1, mobile_width))
rgbB = np.reshape(rgbB, (-1, mobile_width))
rgb[:, :, 0] = rgbR
rgb[:, :, 1] = rgbG
rgb[:, :, 2] = rgbB
cv2.imshow("hud", rgb)
cv2.waitKey()
cv2.imwrite('hud2.png', rgb)

# # output image
# rgb_r = np.reshape(rgb[:, :, 0], (m, -1))
# rgb_g = np.reshape(rgb[:, :, 1], (m, -1))
# rgb_b = np.reshape(rgb[:, :, 2], (m, -1))
# rgbR = W.dot(rgb_r).clip(0, 255)
# rgbG = W.dot(rgb_g).clip(0, 255)
# rgbB = W.dot(rgb_b).clip(0, 255)
# rgbR = np.reshape(rgbR, (-1, mobile_width))
# rgbG = np.reshape(rgbG, (-1, mobile_width))
# rgbB = np.reshape(rgbB, (-1, mobile_width))
# rgb[:, :, 0] = rgbR
# rgb[:, :, 1] = rgbG
# rgb[:, :, 2] = rgbB
# cv2.imshow("hud", rgb)
# cv2.waitKey()

