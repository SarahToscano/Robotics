import matplotlib.pyplot as plt

def plotGraph(x, y, title,  type):
    plt.plot(x,y, type, linewidth=3,label='')
    plt.title(title)
    file_name = title + '.png'
    plt.savefig(file_name, format='png')
    plt.show()