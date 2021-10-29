class Ponto:
    def __init__(self,cores, y, x):
        self.cor = cores[0]
        self.y = y
        self.x = x

def notInRetangule(ponto, retangulos):
    for retang in retangulos:
        if(ponto.x >= retang[0].x and ponto.x <= retang[1].x and ponto.y <= retang[0].y and ponto.y >= retang[1].y):
            return False
    
    return True