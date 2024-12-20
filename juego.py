import pygame  # para la creacion de nuestro juego
import random  # numeros random --> definiremos la posicion de las cartas de manera aleatoria
import os  # para acceder a la carpeta de las imagenes

# iniciamos Pygame
pygame.init()

# configuramos las dimensiones de la ventana
ancho, alto = 600, 600
ventana = pygame.display.set_mode((ancho, alto))

# colores q vamos a tener dentro de la ventana
WHITE, BLACK, BLUE, GRAY = (255, 255, 255), (0, 0, 0), (0, 0, 255), (169, 169, 169)
# fuente_juego = "PressStart2P-Regular.ttf"  PQQQQQQQQ NO FUNCIONASSSSS
FONT = pygame.font.Font(None, 36)

# Configuración del tablero
filas, columnas = (
    4,
    4,
)  # Definir las filas y columnas del tablero donde se van a encontrar las cartas
tamanio_cartas = ancho // columnas

# Cargar imágenes de cartas desde la carpeta 'assets'
assets_carpeta = os.path.join(os.path.dirname(__file__), "assets")
cartas = [
    pygame.image.load(os.path.join(assets_carpeta, f"{i}.jpg")) for i in range(1, 9)
]


# adaptamos el tamaño de las cartas para q se ajustes al tablero
def cambiar_cartas_size(cartas, tamanio):
    return [pygame.transform.scale(carta, (tamanio, tamanio)) for carta in cartas]


# Crear cartas
def crear_cartas(cartas, tamanio_cartas, filas, columnas):
    redimensionadas = cambiar_cartas_size(cartas, tamanio_cartas)
    pareja_cartas = (
        redimensionadas * 2
    )  # duplicamos cada una de las cartas para podamos encontrar las parejas en el juego
    random.shuffle(
        pareja_cartas
    )  # cada vez q el juego se este inicializando --> las cartas serán mezcladas aleatoriamente --> las duplicadas tmb :v

    tablero_cartas = []  # nos creamos el tablero vacio --> inicio del juego
    # dividimos las cartas en filas --> tantas FILAS como haya
    for i in range(filas):
        inicio = i * columnas
        fin = inicio + columnas
        fila = pareja_cartas[inicio:fin]
        tablero_cartas.append(fila)

    return tablero_cartas


# ventana de BIENVENIDA :)
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


# creacion del tablero
def tablero():
    ventana.fill(WHITE)
    for row in range(filas):
        for col in range(columnas):
            x, y = col * tamanio_cartas, row * tamanio_cartas
            if cartas_reveladas[row][col]:
                ventana.blit(board[row][col], (x, y))
            else:
                pygame.draw.rect(
                    ventana, GRAY, (x, y, tamanio_cartas, tamanio_cartas), 3
                )  # Añade borde alrededor de cada carta no revelada
    pygame.display.flip()


def comprobar_pareja_cartas(selected):
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if board[r1][c1] == board[r2][c2]:
            return True
        else:
            pygame.time.wait(1000)
            cartas_reveladas[r1][c1] = True #false
            cartas_reveladas[r2][c2] = True #false
    return False


def victoria():
    # devolveremos true si hemos revelado todas las cartas --> q será cuando hayamos ganado el juego
    if all(all(row) for row in cartas_reveladas):
        return True


def mostrar_mensaje_victoria():
    ventana.fill(WHITE)
    texto_victoria1 = FONT.render("¡Has ganado! :)", True, BLACK)
    texto_victoria2 = FONT.render("¡Nos vemos en la proxima!", True, BLACK)
    texto_victoria3 = FONT.render(f"Pulsaciones totales: {pulsaciones}", True, BLACK)
    ventana.blit(texto_victoria1, (ancho // 2, alto // 3))
    ventana.blit(texto_victoria2, (ancho // 3, alto // 2))
    ventana.blit(texto_victoria3, (10,10)) 
    pygame.display.flip()
    pygame.time.wait(3000)


board = crear_cartas(cartas, tamanio_cartas, filas, columnas)
cartas_reveladas = [
    [False] * columnas for _ in range(filas)
]  # todas las cartas inicialmente ocultas --- inicio

# bucle principal de ejecución en el programa
en_ejecucion = True
selected = []
mostrar_titulo_ventana = True  # Controla si se muestra la pantalla inicial
pulsaciones = 0 #contador de pulsaciones

while en_ejecucion:
    if mostrar_titulo_ventana:
        ventana_inicial()
        for event in pygame.event.get():
            # con le objeto event cogemos las acciones o pulsaciones con las que se pueden encontrar los usuarios

            if event.type == pygame.QUIT:  # 1º accion de salida del juego
                en_ejecucion = False
            if (
                event.type == pygame.MOUSEBUTTONDOWN
            ):  # 2º event del usuario --> btn pulsado
                mostrar_titulo_ventana = False
    else:
        ventana.fill(WHITE)
        tablero()
        #mostramos las pulsaciones y q se vayan actualizando cada vez q pulsamos 
        texto_pulsaciones = FONT.render(f"Pulsaciones: {pulsaciones}", True, BLACK)
        ventana.blit(texto_pulsaciones, (10, 10))
        
        pygame.display.flip()#esto es lo que nos permite la actualizacion de la variable cada vez q el usuario selecciona una carta

        for event in pygame.event.get():
            # volvemos a coger los eventos segun las condiciones :)

            if event.type == pygame.QUIT:  # 1º salimos del juego
                en_ejecucion = False

            ##//SI DETECTAMPS Q EL RATON HA SIDO PULSADO --> ejecutaremos el codigo
            if (
                event.type == pygame.MOUSEBUTTONDOWN
            ):  # 2º cogemos la pulsacion con el raton del usuario
                pulsaciones += 1
                x, y = event.pos
                # 3º pillamos la posicion de dnd se encuentra el ratón  --> q está siendo manejado por el usuario --> con las posiciones "X" e "Y"
           
                ##----------------------
                #calculamos la posición de la carta en filas y columnas
                fila = y // tamanio_cartas  #con esto sabemos en q FILA hemos echo el click
                columna = x // tamanio_cartas  #y aqui en la COLUMNA

                #comprobacion de la carta  --> está oculta
                if not cartas_reveladas[fila][columna]:
                    # Si está oculta, revelarla
                    cartas_reveladas[fila][columna] = True

                    #añadimos la carta seleccionada a la lista de seleccionadas
                    selected.append((fila, columna))

                    #Comprobamos si hay dos cartas seleccionadas
                    if len(selected) == 2:
                        # revisamos si son iguales
                        son_pareja = comprobar_pareja_cartas(selected)
                        if not son_pareja:
                            # Si no son iguales, ocultarlas de nuevo
                            fila1, columna1 = selected[0]  # Primera carta seleccionada
                            fila2, columna2 = selected[1]  # Segunda carta seleccionada

                            cartas_reveladas[fila1][columna1] = False  #ocultamos carta 1
                            cartas_reveladas[fila2][columna2] = False  #ocultamos carta 2

                        #vaciamos nuestro array de cartas seleccionadas para dar paso al  siguiente turno :)
                        selected = []

                if victoria():
                    mostrar_mensaje_victoria()
                    en_ejecucion = False
                    # la variable de q el juego este en marcha la ponemos en FALSE para que deje de ejecutarse y se cierre automaticamente
pygame.quit()
