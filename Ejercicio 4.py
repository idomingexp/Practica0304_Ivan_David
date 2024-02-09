import pygame
from random import randint, uniform

pygame.init()
ventana = pygame.display.set_mode((1200,673))
pygame.display.set_caption("Ejemplo 4")

#Cargamos el fondo de la ventana
fondo = pygame.image.load("fondo.jpg")
ventana.blit(fondo, (0,0))
game_over = pygame.image.load("game-over.png")
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()
#Nos introduce una velocidad distinta de la pelota
#en cada ejecución del juego
speed = [randint(3,6),randint(3,6)]
ballrect.move_ip(0,0)

barra = pygame.image.load("bate.png")
barrarect = barra.get_rect()
barrarect.move_ip(600,600)
golpes = 4
golpes_barra = 0
fuente = pygame.font.Font(None, 36)

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-4,0)
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(4,0)

    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]
        #Aquí hacemos que cada 4 golpes la velocidad de la bola
        #aumente un 20 por ciento 
        golpes_barra = golpes_barra + 1
        if golpes_barra % golpes == 0:
            speed[0] *= 1.2

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
        ventana.fill((252, 243, 207))
        ventana.blit(fondo, (0,0))
        ventana.blit(ball, ballrect)
        ventana.blit(barra, barrarect)

    if barrarect.left < 0:
       barrarect = barrarect.move(4,0)
    if barrarect.right > 1200:
        barrarect = barrarect.move(-4,0)
    
    pygame.display.flip()
    pygame.time.Clock().tick(144)

pygame.quit()
