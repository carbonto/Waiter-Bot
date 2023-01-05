# Waiter-Bot 🤖️🍹️
Se trata de un aplicación del turtlebot para convertirlo en un robot camarero, a traves de ROS y una interfaz.
## Comenzando 🚀
Estas intrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propositos de desarrollo y pruebas.
### Pre-Requisitos 📋
Para la ejecución del software es necesario tener instalado en nuestro dispositivo ros noetic y 
el Turtlebot3. Para su instalación utilizamos los comandos a continuación

```
sudo apt install ros-noetic-desktop-full
sudo apt install ros-noetic-turtlebot3
```
Para mas información de la instalación consultar 

* [Ros Instalation](http://wiki.ros.org/noetic/Installation/Ubuntu) - Instalación de Ros Noetic
* [Turtlebot3 Instalation](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) - Instalación Turtlebot3

### Instalación 🔧
Para tener nuestro Waiter-Bot ejecutandose en nuestro ordenador tenemos que clonar e instalar el repositorio para ello realizamos los siguientes pasos

```
cd catkin_ws/src
git clone https://github.com/carbonto/Waiter-Bot.git
cd ..
catkin build or catkin_make
source devel/setup.bash
```
## Ejecutando las pruebas ⚙️
Para lanzar el entorno simulado del costa coffee tenemos que cargar la simulacion en gazebo y los waypoints ya cargados de cada una de la mesas.

```
roslaunch waiter_bot gazebo_costa_sim.launch
roslaunch waiter_bot waypoints.launch map_name:="mapa_costa_coffee"
```
Una vez lanzado se podrá manejar el robot a través de la interfaz y ver la camara para seguirlo en tiempo real dando en el boton de la camara.
### Mapa Simulacion 🗺️
El mapa que se ha creado para la simulación es un costa coffee realizado mediante la herramienta builder de gazebo y modelados realizados en blender e importados a 
urdf.xacro
![](/waiter_bot/images/costa_gazebo.png)
El mapeado se ha creado utilizando la biblioteca de [Yael Ben Shalom](https://github.com/YaelBenShalom/Turtlebot3-Navigation-with-SLAM#usage-and-configuration-instructions)
el cual hemos obtenido el siguiente resultado.
![](/waiter_bot/images/mapa_costa_coffee.png)
### Interfaz 🖥️
Cuando se lanza el entorno simulado se lanza la interfaz de usuario que se puede ver en la siguiente imagen.
![](/waiter_bot/images/interfaz.jpeg)
La interfaz se ha creado en python utilizando KivyMD, ya que esta librería nos permite crear una interfaz de usuario de manera sencilla y con un diseño agradable, ademñas de que nos permite crear aplicaciones multiplataforma.
## Crear waypoints 
Si queremos crear waypoints en un mapa personalizado o añadir al que tenemos que lanzar el rviz añadiendo el mapa que vamos a usar real o simulado y a continuación el siguiente comando.
```
roslaunch waiter_bot only_waypoints.launch
``` 
Despues publicamos el punto mediante publish point. Para guardarlo usamos este comando:
```
rosservice call /waypoints_save_saver "name: 'nombre_waypoint'"
```

## Usar en turtlebot 2 real 🐢️
Usando los turtlebot del laboratorio el procedimiento sería el siguiente



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
En nuestro caso el nombre del mapa es laboratorio 5 pero si se usara otro mapa se debería cambiar por el nombre del mapa que se quiera usar.
En el rviz colocamos el tf en base_link para ver la posicion de nuestro robot. 
IMPORTANTE: para visualizar correctamente lo que sigue, fijar en RViz como sistema de coordenadas fixed frame -> map
Si el robot no se mueve, es que no se ha localizado correctamente. Para ello, pulsar en 2D Pose Estimate y colocar el robot en el mapa y hubicarlo correctamente mediante teleop.

Para guardar los waypoints sería el mismo procedimiento que se ha explicado anteriormente.

## Menciones
Si vas a usar cualquiera de los recursos de este repositorio, por favor, menciona a los autores originales.<3
- [David Carbonell Pastor](https://github.com/carbonto)
- [Pablo Coloma]()



