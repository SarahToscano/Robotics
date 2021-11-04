from Ponto import Ponto, notInRetangule
import cv2 as cv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

mapa_aux = cv.imread("../../mapa/map.bmp", 0)  # Imagem em escala de cinza
# Mapa binario, todo valor maior que 0 vai ser levado a ser 255
ret, mapa_aux = cv.threshold(mapa_aux, 0, 255, cv.THRESH_BINARY_INV)
mapaBinario = mapa_aux  


# #cria a dilatação das bordas
kernel = np.ones((4, 4), np.uint8)
img_dilation = cv2.dilate(mapaBinario, kernel, iterations=5)  #numero de vezes que eh feita a convolucao

imgplot = plt.imshow(img_dilation)

cv.imwrite('../../mapa/grid.png', img_dilation)

im = cv.imread("../../mapa/grid.png")  
altura = len(im)
largura = len(im[0])

retangulos = []

#capturando as coordenadas dos retangulos
for i in reversed(range(altura)): #k
	for j in range(largura):        #l
		bottomLeft = Ponto(im[i][j], i, j)

		if bottomLeft.cor == 255 and notInRetangule(bottomLeft, retangulos):
			l = j
			while(l+1 < largura and im[i][l+1][0] == 255):
				l = l + 1
			
			k = i			
			while(k >= 0 and im[k-1][j][0] == 255 and im[k-1][l][0] == 255):
				k = k - 1

			topRight = Ponto(im[k][l], k, l)
			retangulos.append([bottomLeft, topRight])   #adicionando retangulo como obstaculo

	

#ponto inicial: (10, 9) ou (50, 45)
#ponto final:   (80, 63)  ou (400, 315)

arq = open('../../mapa/environment.txt', 'w')
arq.write('50,45;400,315\n') #ponto de inicio e ponto de fim

#escrevendo as coordenadas dos obstaculos
for bottonleft, topright in retangulos:
	arq.write(str(bottonleft.x)+','+str(altura - bottonleft.y)+';'+str(topright.x)+','+str(altura - topright.y)+'\n')	
arq.write('-1')

arq.close()