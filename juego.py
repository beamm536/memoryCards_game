import pygame #para la creacion de nuestro juego
import random #numeros random --> definiremos la posicion de las cartas de manera aleatoria
import os     # para acceder a la carpeta de las imagenes 

#iniciamos Pygame
pygame.init()

#configuramos las dimensiones de la ventana
ancho, alto = 600, 600
ventana = pygame.display.set_mode((ancho, alto))

#colores q vamos a tener dentro de la ventana
WHITE, BLACK, BLUE, GRAY = (255, 255, 255), (0, 0, 0), (0, 0, 255), (169, 169, 169)
#fuente_juego = "PressStart2P-Regular.ttf"  PQQQQQQQQ NO FUNCIONASSSSS
FONT = pygame.font.Font(None, 36)

# Configuración del tablero
filas, columnas = 4, 4  # Definir las filas y columnas del tablero donde se van a encontrar las cartas
tamanio_cartas = ancho // columnas

# Cargar imágenes de cartas desde la carpeta 'assets'
assets_carpeta = os.path.join(os.path.dirname(__file__), 'assets')
cartas = [pygame.image.load(os.path.join(assets_carpeta, f'{i}.jpg')) for i in range(1, 9)]

#adaptamos el tamaño de las cartas para q se ajustes al tablero
def cambiar_cartas_size(cartas, tamanio):
    return [pygame.transform.scale(carta, (tamanio, tamanio)) for carta in cartas]

# Crear cartas
def crear_cartas(cartas, tamanio_cartas, filas, columnas):
    redimensionadas = cambiar_cartas_size(cartas, tamanio_cartas)
    pareja_cartas = redimensionadas * 2 #duplicamos cada una de las cartas para podamos encontrar las parejas en el juego
    random.shuffle(pareja_cartas)   #cada vez q el juego se este inicializando --> las cartas serán mezcladas aleatoriamente --> las duplicadas tmb :v

    tablero_cartas = [] #nos creamos el tablero vacio --> inicio del juego
    #dividimos las cartas en filas --> tantas FILAS como haya
    for i in range (filas):
        inicio = i * columnas
        fin = inicio + columnas
        fila = pareja_cartas[inicio:fin]
        tablero_cartas.append(fila)

    return tablero_cartas

#ventana de BIENVENIDA :)
def ventana_inicial():
    ventana.fill(WHITE)
    title_text = FONT.render("Juego de Memoria", True, BLACK)
    rules_text1 = FONT.render("Encuentra las parejas de cartas.", True, BLACK)
    rules_text2 = FONT.render("Haz clic en una carta para revelarla.", True, BLACK)
    rules_text3 = FONT.render("Si coinciden, se quedan abiertas.", True, BLACK)
    rules_text4 = FONT.render("Si no, se volverán a ocultar.", True, BLACK)
    
    ventana.blit(title_text, (ancho // 4, alto // 4))
    ventana.blit(rules_text1, (ancho // 4, alto // 2))
    ventana.blit(rules_text2, (ancho // 4, alto // 2 + 30))
    ventana.blit(rules_text3, (ancho // 4, alto // 2 + 60))
    ventana.blit(rules_text4, (ancho // 4, alto // 2 + 90))
    pygame.display.flip()

#creacion del tablero
def tablero():
    ventana.fill(WHITE)
    for row in range(filas):
        for col in range(columnas):
            x, y = col * tamanio_cartas, row * tamanio_cartas
            if revealed[row][col]:
                ventana.blit(board[row][col], (x, y))
            else:
                pygame.draw.rect(ventana, GRAY, (x, y, tamanio_cartas, tamanio_cartas), 3)  # Añade borde alrededor de cada carta no revelada
    pygame.display.flip()


def comprobar_pareja_cartas(selected):
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if board[r1][c1] == board[r2][c2]:
            return True
        else:
            pygame.time.wait(1000)
            revealed[r1][c1] = False
            revealed[r2][c2] = False
    return False

def victoria():
    #devolveremos true si hemos revelado todas las cartas --> q será cuando hayamos ganado el juego
    if all(all(row)for row in revealed):        
        return True

def mostrar_mensaje_victoria():
    ventana.fill(WHITE)
    texto_victoria1 = FONT.render("¡Has ganado! :)", True, BLACK)
    texto_victoria2 = FONT.render("¡Nos vemos en la proxima!", True, BLACK)
    ventana.blit(texto_victoria1, (ancho // 2, alto // 3))
    ventana.blit(texto_victoria2, (ancho // 3, alto // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    

board = crear_cartas(cartas, tamanio_cartas, filas, columnas)
revealed = [[False] *  columnas  for _ in range(filas)] #todas las cartas inicialmente ocultas

# Bucle principal
running = True
selected = []
show_title_screen = True  # Controla si se muestra la pantalla inicial

while running:
    if show_title_screen:
        ventana_inicial()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_title_screen = False
    else:
        tablero()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // tamanio_cartas, x // tamanio_cartas
                if not revealed[row][col]:
                    revealed[row][col] = True
                    selected.append((row, col))
                if len(selected) == 2:
                    if not comprobar_pareja_cartas(selected):
                        revealed[selected[0][0]][selected[0][1]] = False
                        revealed[selected[1][0]][selected[1][1]] = False
                    selected = []
                if victoria():
                    mostrar_mensaje_victoria()
                    running = False
                    #la variable de q el juego este en marcha la ponemos en false para que deje de ejecutarse
pygame.quit()
