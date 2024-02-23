import pygame
from random import randint, choice

#definimos la clase ladrillo
class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("ladrillo1.png")

    def golpeado(self):
#Si el ladrillo lo golpeamos se destruye
        self.kill()

    def check_collision(self, ball_rect):
#Comprobamos si el ladrillo es golpeado por la bola
        if self.rect.colliderect(ball_rect):
            self.golpeado()
#Hacemos que la bola al golpear con el ladrillo rebote
            if speed[0] < 0:
                speed[0] = -abs(speed[0])
            if speed[0] > 0:
                speed[0] = abs(speed[0])
            if speed[1] < 0:
                speed[1] = abs(speed[1])
            if speed[1] > 0:
                speed[1] = abs(speed[1])

#Definimos la clase del ladrillo de 2 vidas
class Ladrillo2(Ladrillo):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.hits = 0
        self.image = pygame.image.load("ladrillo2.png")

    def golpeado(self):
        if self.hits == 0:
#Si es el primer golpe lo cambiamos a la imagen de la tierra
            self.hits += 1
            self.image = pygame.image.load("ladrillo1.png")
        else:
#Si es el segundo golpe destruimos el ladrillo
            super().golpeado()

#Definimos la clase del ladrillo de 3 vidas
class Ladrillo3(Ladrillo):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.hits = 0
#Cargamos la imagen de la obsidiana
        self.image = pygame.image.load("ladrillo3.png")

    def golpeado(self):
        if self.hits == 0:
#Si es el primer golpe lo cambiamos a la imagen de la roca
            self.hits += 1
            self.image = pygame.image.load("ladrillo2.png")
        elif self.hits == 1:
#En el segundo golpe lo cambiamos a la imagen de la tierra
            self.hits += 1
            self.image = pygame.image.load("ladrillo1.png")
        else:
#Si es el tercer golpe destruimos el ladrillo
            super().golpeado()

#Definimos la clase del ladrillo irrompible
class Ladrillo4(Ladrillo):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.hits = 0
#Cargamos la imagen de la bedrock
        self.image = pygame.image.load("ladrillo4.png")

    def golpeado(self):
        if self.hits == 0:
            self.hits += 1
            self.image = pygame.image.load("ladrillo4.png")

# Grupo de ladrillos
grupo_ladrillos = pygame.sprite.Group()

#Generamos los ladrillos de manera aleatoria
for y in range(7):
    for x in range(10):
# Elegir aleatoriamente entre las clases de ladrillo disponibles
        ladrillo_class = choice([Ladrillo, Ladrillo2, Ladrillo3, Ladrillo4])
#Creamos la instancia del ladrillo que queremos
        ladrillo = ladrillo_class((255, 0, 0), 100, 20)
#Ponemos el ladrillo en la ventana
        ladrillo.rect.x = x * 155
        ladrillo.rect.y = y * 50
#Agregamos el ladrillo al grupo
        grupo_ladrillos.add(ladrillo)

# Inicialización de Pygame
pygame.init()
ventana = pygame.display.set_mode((1200, 673))
pygame.display.set_caption("MINECRANOID")

# Cargamos imagenes y otras variables
fondo = pygame.image.load("fondo.jpg")
ventana.blit(fondo, (0,0))
game_over = pygame.image.load("game-over.png")
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()
speed = [0,0]
ballrect.move_ip(600,336)
golpes_barra = 0
golpes = 8
barra = pygame.image.load("bate.png")
barrarect = barra.get_rect()
barrarect.move_ip(600,600)
fuente = pygame.font.Font(None, 36)
#Bucle principal de inicio del juego
jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
#Hasta que no pulsemos el espacio no comienza el juego
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and speed == [0, 0]:
                speed = [randint(2, 4), randint(2, 4)]
#Configuramos el movimiento del bate
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-5,0)
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(5,0)
#Comprobamos si la bola y el bate colisionan y cada 8 golpes subimos
#la velocidad un 5%
    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]
        golpes_barra += 1
        if golpes_barra % golpes == 0:
            speed[0] *= 1.05
            speed[1] *= 1.05
#Comprobamos las colisiones de la bola con las paredes
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0: 
        speed[1] = -speed[1]
    if ballrect.bottom > ventana.get_height():
        ventana.fill((0, 0, 0))
        ventana.blit(game_over, (0, 0))
        texto = fuente.render("Has Muerto", True, (255,255,255))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
#Dibujamos el fondo y cargamos los ladrillos, bola y barra    
    else:
        ventana.blit(fondo, (0,0))
        grupo_ladrillos.draw(ventana)
        ventana.blit(ball, ballrect)
        ventana.blit(barra, barrarect)
        for ladrillo in grupo_ladrillos.sprites():
            ladrillo.check_collision(ballrect)
#Hacemos que la barra no salga de la ventana de juego
    if barrarect.left < 0:
       barrarect = barrarect.move(5,0)
    if barrarect.right > 1200:
        barrarect = barrarect.move(-5,0)

    pygame.display.flip()
    pygame.time.Clock().tick(144)

pygame.quit()