import pygame
from random import randint, choice

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("ladrillo1.png")

    def golpeado(self):
        self.kill()

    def check_collision(self, ball_rect):
        if self.rect.colliderect(ball_rect):
            self.golpeado()
            if speed[0] < 0:
                speed[0] = abs(speed[0])
            else:
                speed[0] = -abs(speed[0])
            if speed[1] < 0:
                speed[1] = abs(speed[1])
            else:
                speed[1] = -abs(speed[1])

class Ladrillo2(Ladrillo):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.hits = 0
        self.image = pygame.image.load("ladrillo2.png")
    def golpeado(self):
        if self.hits == 0:
            self.hits += 1
            self.image = pygame.image.load("ladrillo1.png")

        else:
            super().golpeado()

class Ladrillo3(Ladrillo):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.hits = 0
        self.image = pygame.image.load("ladrillo3.png")
    def golpeado(self):
        if self.hits == 0:
            self.hits += 1
            self.image = pygame.image.load("ladrillo2.png")
        elif self.hits == 1:
            self.hits += 1
            self.image = pygame.image.load("ladrillo1.png")

        else:
            super().golpeado()

class Ladrillo4(Ladrillo):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.hits = 0
        self.image = pygame.image.load("ladrillo4.png")
    def golpeado(self):
        if self.hits == 0:
            self.hits += 1
            self.image = pygame.image.load("ladrillo4.png")
        else:
            self.hits += 1
            self.image = pygame.image.load("ladrillo4.png")

grupo_ladrillos = pygame.sprite.Group()

for j in range(7):
    for i in range(10):
        ladrillo_class = choice([Ladrillo, Ladrillo2, Ladrillo3])
        ladrillo = ladrillo_class((255, 0, 0), 100, 20)
        ladrillo.rect.x = i * 155
        ladrillo.rect.y = j * 50
        grupo_ladrillos.add(ladrillo)

pygame.init()
ventana = pygame.display.set_mode((1200, 673))
pygame.display.set_caption("Ejemplo 4")

fondo = pygame.image.load("fondo.jpg")
ventana.blit(fondo, (0,0))
game_over = pygame.image.load("game-over.png")
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()
speed = [0,0]
ballrect.move_ip(600,336)
golpes_barra = 0
golpes = 4
barra = pygame.image.load("bate.png")
barrarect = barra.get_rect()
barrarect.move_ip(600,600)
fuente = pygame.font.Font(None, 36)

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and speed == [0, 0]:
                speed = [randint(2, 4), randint(2, 4)]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-4,0)
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(4,0)

    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]
        speed[1] *= 1.05
        golpes_barra += 1
        if golpes_barra % golpes == 0:
            speed[0] *= 1.1

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
    
    else:
        ventana.blit(fondo, (0,0))
        grupo_ladrillos.draw(ventana)
        ventana.blit(ball, ballrect)
        ventana.blit(barra, barrarect)
        for ladrillo in grupo_ladrillos.sprites():
            ladrillo.check_collision(ballrect)

    if barrarect.left < 0:
       barrarect = barrarect.move(4,0)
    if barrarect.right > 1200:
        barrarect = barrarect.move(-4,0)

    pygame.display.flip()
    pygame.time.Clock().tick(144)

pygame.quit()
