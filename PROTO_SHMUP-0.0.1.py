'''TP Final POO, Proto Shmup, shooter vertical en pygame
'''
import pygame
import random
from os import path

#Constantes Generales
TITULO = 'Prototipo de Shoot\'Em Up'

#Atributos meteoro
METEOR_SIZES = [20, 40, 40, 60]

#Atributos Player
SPEED  = 8
SPREAD = [-2, 0, 2] #valores de velocidad x del disparo tipo spread


WIDTH = 480
HEIGHT = 640
#atributos screen
BORDE_RIGHT = int(WIDTH * 0.95) #limites máximos y mínimos
BORDE_LEFT = int(WIDTH * 0.05)  # del movimiento de la nave
BORDE_TOP = int(HEIGHT * 0.1)
BORDE_BOTTOM = int(HEIGHT * 0.8)
FPS = 60


#clases

        

class Player(pygame.sprite.Sprite): #hereda de pygame.sprite.Sprite
    '''Atributos para la Nave'''

    def __init__(self, game):
        pygame.sprite.Sprite.__init__( self)
        self.image = pygame.transform.scale(game.player_img, (32, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.y = int(HEIGHT*0.95)
        self.speed_x = 0    
        self.speed_y = 0
        self.speed = SPEED
        self.last_bullet_shot = pygame.time.get_ticks()
    
    def disparar(self, game):
        '''crea y dispara bala'''
        current_time = pygame.time.get_ticks() #configuración autodisparo
        if current_time - self.last_bullet_shot > 100:
            self.last_bullet_shot = current_time
            b = bullet(game, self.rect.centerx, self.rect.top, 0)
            game.all_bullets.add(b)
            game.all_sprites.add(b)

    def disparar_spread(self, game):
            '''crea y dispara rafaga de balas'''
            current_time_spread = pygame.time.get_ticks()
            if current_time_spread - self.last_bullet_shot > 120:
                self.last_bullet_shot = current_time_spread                
                for i in SPREAD:
                    b = bullet(game, self.rect.centerx, self.rect.top, i)
                    game.all_bullets.add(b)
                    game.all_sprites.add(b)

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
        
        self.speed_x = 0
        self.speed_y = 0
        self.modo_focus = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_d]:
            self.disparar_spread(game)
            self.modo_focus = 3
        if keystate[pygame.K_RIGHT]:
            self.speed_x = self.speed - self.modo_focus
        if keystate[pygame.K_LEFT]:
            self.speed_x = -self.speed + self.modo_focus
        if keystate[pygame.K_UP]:
            self.speed_y = -self.speed + self.modo_focus
        if keystate[pygame.K_DOWN]:
            self.speed_y = self.speed - self.modo_focus
        


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def update(self):
        self.moverse()
        self.bordes()

class Meteoro(pygame.sprite.Sprite):
    '''Atributos de los meteoros'''

    def __init__(self, game, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(game.meteor_img, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-400, 0)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)

    def spawn_new_meteor(self):
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(-400, 0)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)
        

    def bordes(self):
         """Respawn si se va de la pantalla"""
         if self.rect.left > WIDTH + 60 or self.rect.right < - 60 or self.rect.bottom > HEIGHT + 60:
             self.spawn_new_meteor()
    
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.bordes()
        


class bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, bullet_x_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.laser_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed_y = -15
        self.speed_x = bullet_x_speed

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

class Splash_Screen:
    def __init__(self, logo_path, screen):
        self.screen = screen
        pygame.display.set_caption(TITULO)
        #self.clock = pygame.time.Clock() no implementado al ser imagenes fijas
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.logo = pygame.image.load(path.join(self.img_folder, logo_path)).convert()

    def show(self):
        mostrar = True
        while mostrar:
            #self.clock.tick(FPS)
            self.screen.blit(self.logo, (0, (HEIGHT/2) - self.logo.get_height()/2))       
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    mostrar = False
                if event.type == pygame.QUIT:
                    mostrar = False
            pygame.display.update()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.background = self.get_image("background.png")
        self.background_rect = self.background.get_rect()
        self.player_img = self.get_image("playership.png")
        self.laser_img = self.get_image("laser.png")
        self.meteor_img = self.get_image("asteroid.png")
        self.total_meteors = 30
        #Sprites
        self.all_sprites = pygame.sprite.Group() #Contenedor para TOODOS los sprites
        self.all_meteors =  pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()
        self.nave = Player(self)
        self.all_sprites.add(self.nave)

    def create_meteors(self, cantidad):
        for i in range(cantidad):
            m = Meteoro(self, random.choice(METEOR_SIZES))
            self.all_meteors.add(m)
            self.all_sprites.add(m)

    def spawn_new_meteor(self):
        m = Meteoro(self, random.choice(METEOR_SIZES))
        self.all_meteors.add(m)
        self.all_sprites.add(m)

    def get_image(self, filename):
        img = pygame.image.load(path.join(self.img_folder, filename)).convert_alpha()
        return img
    
    def run(self):
        running = True
        self.create_meteors(8)
        total_meteors = 40
        luifa = Splash_Screen('luifagames_logo.png', self.screen)
        unpi = Splash_Screen('logo_unpilar.png', self.screen)
        title = Splash_Screen('title_screen.png', self.screen)
        perder = Splash_Screen('perdiste.png', self.screen)
        ganar = Splash_Screen('ganaste.png', self.screen)
        creditos = Splash_Screen('creditos.png', self.screen)
        
        luifa.show()
        unpi.show()
        title.show()
        while running:

            self.clock.tick(FPS) #mantiene al juego corriendo a 60fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.nave.disparar(self)#implementar el disparo acá es un poco desprolijo pero como funciona y se acerca la hora de entrega se deja así
            #Actualiza
            self.all_sprites.update()

            #Chequear colisiones
            colision_meteoro = pygame.sprite.spritecollide(self.nave, self.all_meteors, False)
            if colision_meteoro:
                running = False
            
            bullet_collision = pygame.sprite.groupcollide(self.all_meteors, self.all_bullets, True, True)

            if bullet_collision and total_meteors > 0:
                self.spawn_new_meteor()
                total_meteors -=1
            if total_meteors == 0:
                running = False

            self.screen.blit(self.background, self.background_rect)
            self.all_sprites.draw(self.screen)
            #Actualiza después de dibujar todo en pantalla
            pygame.display.update()
        if total_meteors == 0:
            ganar.show()
        else: perder.show()
        creditos.show()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()