# Waiter-Bot 馃锔忦煃癸笍
Se trata de un aplicaci贸n del turtlebot para convertirlo en un robot camarero, a traves de ROS y una interfaz.
## Comenzando 馃殌
Estas intrucciones te permitir谩n obtener una copia del proyecto en funcionamiento en tu m谩quina local para propositos de desarrollo y pruebas.
### Pre-Requisitos 馃搵
Para la ejecuci贸n del software es necesario tener instalado en nuestro dispositivo ros noetic y 
el Turtlebot3. Para su instalaci贸n utilizamos los comandos a continuaci贸n

```
sudo apt install ros-noetic-desktop-full
sudo apt install ros-noetic-turtlebot3
```
Para mas informaci贸n de la instalaci贸n consultar 

* [Ros Instalation](http://wiki.ros.org/noetic/Installation/Ubuntu) - Instalaci贸n de Ros Noetic
* [Turtlebot3 Instalation](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) - Instalaci贸n Turtlebot3

### Instalaci贸n 馃敡
Para tener nuestro Waiter-Bot ejecutandose en nuestro ordenador tenemos que clonar e instalar el repositorio para ello realizamos los siguientes pasos

```
cd catkin_ws/src
git clone https://github.com/carbonto/Waiter-Bot.git
cd ..
catkin build or catkin_make
source devel/setup.bash
```
## Ejecutando las pruebas 鈿欙笍
Para lanzar el entorno simulado del costa coffee tenemos que cargar la simulacion en gazebo y los waypoints ya cargados de cada una de la mesas.

```
roslaunch waiter_bot gazebo_costa_sim.launch
roslaunch waiter_bot waypoints.launch map_name:="mapa_costa_coffee"
```
Una vez lanzado se podr谩 manejar el robot a trav茅s de la interfaz y ver la camara para seguirlo en tiempo real dando en el boton de la camara.
### Mapa Simulacion 馃椇锔?
El mapa que se ha creado para la simulaci贸n es un costa coffee realizado mediante la herramienta builder de gazebo y modelados realizados en blender e importados a 
urdf.xacro
![](/waiter_bot/images/costa_gazebo.png)
El mapeado se ha creado utilizando la biblioteca de [Yael Ben Shalom](https://github.com/YaelBenShalom/Turtlebot3-Navigation-with-SLAM#usage-and-configuration-instructions)
el cual hemos obtenido el siguiente resultado.
![](/waiter_bot/images/mapa_costa_coffee.png)
### Interfaz 馃枼锔?
Cuando se lanza el entorno simulado se lanza la interfaz de usuario que se puede ver en la siguiente imagen.
![](/waiter_bot/images/interfaz.jpeg)
La interfaz se ha creado en python utilizando KivyMD, ya que esta librer铆a nos permite crear una interfaz de usuario de manera sencilla y con un dise帽o agradable, adem帽as de que nos permite crear aplicaciones multiplataforma.
## Crear waypoints 
Si queremos crear waypoints en un mapa personalizado o a帽adir al que tenemos que lanzar el rviz a帽adiendo el mapa que vamos a usar real o simulado y a continuaci贸n el siguiente comando.
```
roslaunch waiter_bot only_waypoints.launch
``` 
Despues publicamos el punto mediante publish point. Para guardarlo usamos este comando:
```
rosservice call /waypoints_save_saver "name: 'nombre_waypoint'"
```

## Usar en turtlebot 2 real 馃悽锔?
Usando los turtlebot del laboratorio el procedimiento ser铆a el siguiente



```
Configuracion de tu bashrc previo
ssh turtlebot@ipturtlebot
roslaunch turtlebot_bringup minimal.launch
roslaunch turtlebot_bringup hokuyo_ust10lx.launch
Pasamos el mapa
scp archivo turtlebot@laIP:direccion 
export TURTLEBOT_3D_SENSOR=astra
roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/turtlebot/fichero_de_tu_mapa.yaml
```
Desde nuestro terminal lanzamos los siguientes comandos 

```
roslaunch waiter_bot real.launch map_name:="laboratorio_5"
rosrun rviz rviz 
```
En nuestro caso el nombre del mapa es laboratorio 5 pero si se usara otro mapa se deber铆a cambiar por el nombre del mapa que se quiera usar.
En el rviz colocamos el tf en base_link para ver la posicion de nuestro robot. 
IMPORTANTE: para visualizar correctamente lo que sigue, fijar en RViz como sistema de coordenadas fixed frame -> map
Si el robot no se mueve, es que no se ha localizado correctamente. Para ello, pulsar en 2D Pose Estimate y colocar el robot en el mapa y hubicarlo correctamente mediante teleop.

Para guardar los waypoints ser铆a el mismo procedimiento que se ha explicado anteriormente.

## Menciones
Si vas a usar cualquiera de los recursos de este repositorio, por favor, menciona a los autores originales.<3
- [David Carbonell Pastor](https://github.com/carbonto)
- [Pablo Coloma]()



