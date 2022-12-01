# Waiter-Bot
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


