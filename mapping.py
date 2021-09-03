from Ponto import Ponto
import cv2 as cv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

mapa_aux = cv.imread("map.bmp", 0)  # Imagem em escala de cinza
# Binarizing map, first we force 255 to any value higher than 0
ret, mapa_aux = cv.threshold(mapa_aux, 0, 255, cv.THRESH_BINARY_INV)
mapaBinario = mapa_aux  # // 255 # Then we divine by 255, so we have 0s and 1s


# Esse algoritmo faz o redimensionamento na escala mas o segundo achei que ficou melhor
# algoritmo que diminui a resolução
# scale_percent = 5
# width = int(mapaBinario.shape[1] / scale_percent )
# height = int(mapaBinario.shape[0] / scale_percent)
# dim = (width, height)

# funcao do opencv que redimensiona a escala
# resized = cv2.resize(mapaBinario, dim, interpolation = cv2.INTER_AREA)
resolucao = 5

# cria uma nova matriz de zeros do tamanho da nova escala
size = int(mapaBinario.shape[0]/resolucao), int(mapaBinario.shape[1]/resolucao)
mapaCells = np.zeros(size, dtype=np.uint8)


# preenche essa nova matriz de zeros redimensionada
for (i, m) in zip(range(mapaCells.shape[0]), range(0, mapaBinario.shape[0] + 1, 5)):
    for (j, n) in zip(range(mapaCells.shape[1]), range(0, mapaBinario.shape[1] + 1, 5)):
        mapaCells[i, j] = mapaBinario[m, n]

# #cria a dilatação das bordas, no caso engorda
kernel = np.ones((4, 4), np.uint8)
# print(kernel)
img_dilation = cv2.dilate(mapaCells, kernel, iterations=1)

# num = {}
# for i in range(72):
#     for j in range(90):
#         if img_dilation[i][j] in num:
#             num[img_dilation[i][j]] = num[img_dilation[i][j]] + 1
#         else:
#             num[img_dilation[i][j]] = 1
# print(num)

imgplot = plt.imshow(img_dilation)

cv.imwrite('grid.png', img_dilation)

im = cv.imread("grid.png")  # {0: 4254, 255: 2226}
altura = len(im)
largura = len(im[0])

visitados = []
a = 0

for i in reversed(range(altura)):
	for j in range(largura):
		ponto = Ponto(im[i][j])

		if ponto.cores[0] == 255 and ponto not in visitados:
			visitados.append(ponto)
			k = i - 1
			l = j + 1

			while l < largura and k >= 0 and im[k][l][0] == 255:
				#print('k = '+str(k)+' e l = '+str(l))

				visitados.append(Ponto(im[k][l]))
				visitados.append(Ponto(im[k+1][l]))
				visitados.append(Ponto(im[k][l-1]))
				k = k - 1
				l = l + 1
				


			cv.line(im, (j, i), (l-1, k+1), (0, 255, 0), 1)

cv.imwrite('gridDraw.png', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
