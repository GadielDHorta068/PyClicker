# Automatización de Clicks en Pantalla
## Este proyecto está diseñado para detectar y hacer clic en el objeto de mayor tamaño en movimiento en la pantalla utilizando Python

### Instalación de Dependencias
Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes bibliotecas de Python:

pip install pyautogui opencv-python numpy keyboard setproctitle


### Ejecución:

Ejecuta el script main.py.
Presiona la tecla 's' para iniciar la detección y clics en pantalla.
Para detener el programa, presiona la tecla 'q'.

Adicional, puedes encontrar un ejecutable en \clicker\dist\. El mismo se puede crear realizando
pyinstaller --onefile detector_objeto.py

### Configuración Adicional:

El programa se ejecuta en pantalla completa y está configurado para buscar y hacer clic en el objeto de mayor tamaño en movimiento después de esperar la tecla 's' para iniciar.
Funcionalidades
Detección de Objetos en Movimiento: Utiliza OpenCV para capturar y procesar imágenes de la pantalla en busca de objetos en movimiento.

Control de Clics en Pantalla: Utiliza PyAutoGUI para realizar clics en las coordenadas del objeto detectado.

Control de Proceso: Utiliza setproctitle para establecer el nombre del proceso durante la ejecución.

### Contribución
Si deseas contribuir a este proyecto, sigue estos pasos:

Haz un fork del repositorio.
Crea una nueva rama (git checkout -b feature-nueva-funcionalidad).

Haz commit de tus cambios (git commit -am 'Agrega una nueva funcionalidad').

Sube tus cambios (git push origin feature-nueva-funcionalidad).

Abre un pull request.