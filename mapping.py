import cv2 as cv
import cv2
import numpy as np
import matplotlib.pyplot as plt 


#imagem original
mapa = cv.imread("map.bmp")
#cv.imshow("Original map", mapa)
#cv.waitKey(0)

mapa_aux = cv.imread("map.bmp", 0) # Imagem em escala de cinza
        #Binarizing map, first we force 255 to any value higher than 0
ret, mapa_aux = cv.threshold(mapa_aux, 0, 255, cv.THRESH_BINARY_INV)
mapaBinario = mapa_aux // 255 # Then we divine by 255, so we have 0s and 1s

   
 #Used for proportion of AStar cells
############################## Esse algoritmo faz o redimensionamento na escala mas o segundo achei que ficou melhor
#algoritmo que diminui a resolução
#scale_percent = 5 # percent of original size
#width = int(mapaBinario.shape[1] / scale_percent )
#height = int(mapaBinario.shape[0] / scale_percent)
#dim = (width, height)

#funcao do opencv que redimensiona a escala
#resized = cv2.resize(mapaBinario, dim, interpolation = cv2.INTER_AREA)
resolucao = 5

        #cria uma nova matriz de zeros do tamanho da nova escala
size = int(mapaBinario.shape[0]/resolucao), int(mapaBinario.shape[1]/resolucao)
mapaCells = np.zeros(size, dtype=np.uint8)


        #preenche essa nova matriz de zeros redimensionada        
for (i, m) in zip(range(mapaCells.shape[0]), range(0 , mapaBinario.shape[0] +1, 5)):
    for (j, n) in zip(range(mapaCells.shape[1]), range(0 , mapaBinario.shape[1] +1, 5)):
        mapaCells[i, j] = mapaBinario[m, n]

        #cria a dilatação das bordas, no caso engorda
kernel = np.ones((5,5), np.uint8)
img_dilation = cv2.dilate(mapaCells, kernel, iterations=1) 


imgplot = plt.imshow(img_dilation)
plt.show()



    
