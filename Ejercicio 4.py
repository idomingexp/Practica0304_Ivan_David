import pygame
from random import randint

#Nos indica la separación entre los ladrillos
hueco_x = 600 / 6 + 600 / 36
#creamos la clase ladrillo
class Ladrillo:
    def __init__(self, imagen, filas, columnas):
        self.__imagen = pygame.image.load(imagen)
        self.__rect = self.__imagen.get_rect()
        self.__ladrillos = []

        for y in range(filas):
            ladrilloY = y * (self.__rect.height + 20)
            for x in range(columnas):
                ladrilloX = x * (self.__rect.width + hueco_x)
                self.__ladrillos.append((ladrilloX, ladrilloY))

    @property
    def imagen(self):
        return self.__imagen
    
    @imagen.setter
    def imagen(self, valor):
        self.__imagen = valor

    def dibujar_ladrillos(self, ventana):
        for pos in self.__ladrillos:
            ventana.blit(self.__imagen, pos)

# Inicialización de Pygame
pygame.init()
ventana = pygame.display.set_mode((1200, 673))
pygame.display.set_caption("Ejemplo 4")

#Cargamos el fondo de la ventana
fondo = pygame.image.load("fondo.jpg")
ventana.blit(fondo, (0,0))
game_over = pygame.image.load("game-over.png")
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()
#Nos introduce una velocidad distinta de la pelota
#en cada ejecución del juego
speed = [0,0]
ballrect.move_ip(600,336)

barra = pygame.image.load("bate.png")
barrarect = barra.get_rect()
barrarect.move_ip(600,600)
golpes = 4
golpes_barra = 0
fuente = pygame.font.Font(None, 36)

# Crear instancia de la clase Ladrillo
ladrillo = Ladrillo("Ladrillo1.png", 6, 6)

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and speed == [0, 0]:  # Si se presiona la barra espaciadora y la bola está quieta
                speed = [randint(-4, 4), randint(-4, 4)]  # Asigna una velocidad aleatoria a la bola
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-4,0)
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(4,0)

    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]
        speed[1] *= 1.05
        #Aquí hacemos que cada 4 golpes la velocidad de la bola
        #aumente un 5 por ciento 
        golpes_barra += 1
        if golpes_barra % golpes == 0:
            speed[0] *= 1.1

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0: 
        speed[1] = -speed[1]
    #Nos indica que al tocar abajo ya no rebota más
    if ballrect.bottom > ventana.get_height():
        ventana.fill((0, 0, 0))
        ventana.blit(game_over, (0, 0))
        #Aquí introduce el texto de perder
        texto = fuente.render("Has Muerto", True, (255,255,255))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
        
    else:
        ventana.blit(fondo, (0,0))
        #Aquí tenemos las colisiones entre los ladrillos y la bola
        for i, pos in enumerate(ladrillo._Ladrillo__ladrillos):
            ladrillo_rect = pygame.Rect(pos, (ladrillo._Ladrillo__rect.width, ladrillo._Ladrillo__rect.height))
            if ladrillo_rect.colliderect(ballrect):
                speed[1] = -speed[1]
                # Eliminar el ladrillo colisionado
                del ladrillo._Ladrillo__ladrillos[i]
                break
        ladrillo.dibujar_ladrillos(ventana)
        ventana.blit(ball, ballrect)
        ventana.blit(barra, barrarect)

    if barrarect.left < 0:
       barrarect = barrarect.move(4,0)
    if barrarect.right > 1200:
        barrarect = barrarect.move(-4,0)

    pygame.display.flip()
    pygame.time.Clock().tick(144)

pygame.quit()