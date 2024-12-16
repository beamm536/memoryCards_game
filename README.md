# memoryCards_game

Este es un juego de memoria desarrollado en Python utilizando la biblioteca Pygame. El objetivo del juego es encontrar todas las parejas de cartas lo más rápido posible.

## Características
- **Interfaz visual interactiva:** basada en Pygame.
- **Cartas aleatorias:** cada partida mezcla las cartas de forma diferente.
- **Pantalla inicial:** incluye instrucciones para aprender a jugar.
- **Mensajes de victoria:** cuando completas el juego, se muestra un mensaje de felicitación.

## Requisitos
Para ejecutar este proyecto, necesitas:
- Python 3.x
- La biblioteca Pygame

## Instalación
1. Clona este repositorio o descarga los archivos.
2. Instala Pygame si aún no lo tienes:
   ```bash
   pip install pygame
   ```
3. Asegúrate de tener una carpeta llamada assets en el directorio del proyecto con las imágenes de las cartas. Las imágenes deben estar numeradas del 1.jpg al 9.jpg:

## Cómo jugar
1. Ejecuta el archivo principal del juego:
```bash
python juego_memoria.py
```
2. En la pantalla inicial, lee las instrucciones y haz clic para comenzar.
3. Haz clic en las cartas para revelarlas:
  - Si dos cartas coinciden, permanecerán descubiertas.
  - Si no coinciden, se ocultarán de nuevo tras un momento.
4. Encuentra todas las parejas para ganar! 😊
   
