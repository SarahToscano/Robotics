# nonlinear-model-predictive-controller
 nonlinear model predictive controller for trajectory tracking (NMPC)

O pacote turtlebot3_description serve apenas para ter o modelo do robô usado

Para abrir o robô no mapa no gazebo:

---roslaunch simu spawn.launch
   
Executar o algoritmo NMPC com localização por monte-carlo:

---rosrun simu control.py




Caso queira alterar o ponto de destino:

---mudar os valores da linha 51 do arquivo mapping.py, e executar o arquivo. Em seguida executar o prm.py para refazer a rota
