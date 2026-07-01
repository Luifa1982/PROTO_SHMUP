'''TP Final POO, shooter vertical
-movimiento
-generar enemigos
'''
import pygame
import time
import random
from os import path

#Constantes Generales
TITULO = 'Prototipo'
#Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0 ,0 ,255)
YELLOW = (255, 255, 0)


#Atributos Player
HITBOX = (20, 20)
SPEED  = 8
BULLET_WIDTH = 8#debería ser variable si el player sube de nivel el arma...

pygame.init() #requiere pygame.quit() al final
pygame.mixer.init() #inicializa sonido
WIDTH = 480
HEIGHT = 640
#atributos screen
BORDE_RIGHT = int(WIDTH * 0.95) #limites máximos y mínimos
BORDE_LEFT = int(WIDTH * 0.05)  # del movimiento de la nave
BORDE_TOP = int(HEIGHT * 0.1)
BORDE_BOTTOM = int(HEIGHT * 0.8)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)
clock = pygame.time.Clock()
FPS = 60
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")

#clases
class Player(pygame.sprite.Sprite):
    '''Atributos para la Nave'''

    def __init__(self):
        pygame.sprite.Sprite.__init__( self)
        self.image = pygame.transform.scale(player_img, (32, 48))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.y = int(HEIGHT*0.95)
        self.speed_x = 0    #revisar para que funcione con solo una variable
        self.speed_y = 0
        self.speed = SPEED
        self.last_bullet_shot = pygame.time.get_ticks()
    
    def disparar(self):
        '''crea y dispara bala'''
        current_time = pygame.time.get_ticks()#configuración autodisparo
        if current_time - self.last_bullet_shot > 100:
            self.last_bullet_shot = current_time
            b = bullet(self.rect.centerx, self.rect.top, 0)
            all_bullets.add(b)
            all_sprites.add(b)

    def disparar_spread(self):
            current_time_spread = pygame.time.get_ticks()
            if current_time_spread - self.last_bullet_shot > 120:
                self.last_bullet_shot = current_time_spread
                for i in range(-BULLET_WIDTH//2, BULLET_WIDTH//2 + 4, 3):
                    b = bullet(self.rect.centerx, self.rect.top, i)
                    all_bullets.add(b)
                    all_sprites.add(b)

    def bordes(self):
        '''limite movimiento de la nave'''
        if self.rect.right > BORDE_RIGHT:
            self.rect.right = BORDE_RIGHT
        if self.rect.left < BORDE_LEFT:
            self.rect.left = BORDE_LEFT
        if self.rect.top < BORDE_TOP:
            self.rect.top = BORDE_TOP
        if self.rect.bottom > BORDE_BOTTOM:
            self.rect.bottom = BORDE_BOTTOM

    def moverse(self):
        '''Movimiento de la nave'''
        
        self.speed_x = 0 #reinicia velocidad para que la nave se detenga al soltar el botón
        self.speed_y = 0
        self.modo_focus = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_d]:
            self.disparar()
            self.modo_focus = 3 #La nave se desplaza mas despacio, como en juego tipo Cave
        if keystate[pygame.K_RIGHT]:
            self.speed_x = self.speed - self.modo_focus
        if keystate[pygame.K_LEFT]:
            self.speed_x = -self.speed + self.modo_focus
        if keystate[pygame.K_UP]:
            self.speed_y = -self.speed + self.modo_focus
        if keystate[pygame.K_DOWN]:
            self.speed_y = self.speed - self.modo_focus
        #if event.type == pygame.KEYUP and event.key == pygame.K_d:
        #    self.modo_focus = 0 #vuelve a la velocidad doriginal al soltar



        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def update(self):
        self.moverse()
        self.bordes()

class Meteoro(pygame.sprite.Sprite):
    '''Atributos de los meteoros'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, BORDE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(0, BORDE_TOP)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)

    def spawn_new_meteor(self):
        self.rect.x = random.randrange(0, BORDE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(0, BORDE_TOP)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)
        

    def bordes(self):
         """Respawn si se va de la pantalla"""
         if self.rect.left > BORDE_RIGHT + 40 or self.rect.right < BORDE_LEFT - 40 or self.rect.top < BORDE_TOP - 40 or self.rect.bottom > BORDE_BOTTOM + 40:
             self.spawn_new_meteor()
    
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.bordes()
        


class bullet(pygame.sprite.Sprite):#Funciona, falta rotar balas, falta que modo laser no lo pise tanto
    def __init__(self, x, y, bullet_x_speed): #s e y representan el centro de la nave
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((5, 10))
        self.image = laser_img
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed_y = -10
        self.speed_x = bullet_x_speed

    def update(self):
        self.rect.y += self.speed_y * 1.5
        self.rect.x += self.speed_x


#Funciones
def spawn_new_meteor():
    m = Meteoro()
    all_meteors.add(m)
    all_sprites.add(m)

def get_image(filename):
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    return img
#Imagenes
#background = pygame.image.load(path.join(img_folder, "background.png")).convert()
background = get_image("background.png")
background_rect = background.get_rect()
player_img = get_image("playership.png")
laser_img = get_image("laser.png")


#Sprites
all_sprites = pygame.sprite.Group() #Contenedor para TOODOS los sprites
all_meteors =  pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
nave = Player()
all_sprites.add(nave)

for i in range(9):
    m = Meteoro()
    all_meteors.add(m)
    all_sprites.add(m)

#Main loop
running = True
while running:

    clock.tick(FPS) #mantiene al juego corriendo a 60fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                nave.disparar_spread()
    #Actualiza
    all_sprites.update()

    #Chequear colisiones
    colision_meteoro = pygame.sprite.spritecollide(nave, all_meteors, False)
    if colision_meteoro:
        running = False
    
    bullet_collision = pygame.sprite.groupcollide(all_meteors, all_bullets, True, True)

    #Decisiones de diseño de juego que se siguen para completar el tutorial:
    #(A CAMBIAR)

    if bullet_collision:
        spawn_new_meteor()
    #Dibuja en pantalla
    #screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    #Actualiza después de dibujar todo en pantalla
    pygame.display.update()

pygame.quit()
        