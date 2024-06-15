import pygame
import os
import random

# Rutas de archivos desde la carpeta del juego
script_dir = os.path.dirname(os.path.abspath(__file__))
repelente_image_path = os.path.join(script_dir, 'assets/repelente-contra-mosquitos.png')

class ObstaculoStatic(pygame.sprite.Sprite):
    def __init__(self, screen, objetos):
        super().__init__()
        self.screen = screen
        self.objetos = objetos  # Almacena la lista de objetos del nivel
        self.image = pygame.image.load(repelente_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(midright=(self.screen.get_width(), random.randint(50, self.screen.get_height() - 150)))
        self.speed = 17  # Velocidad del obstáculo

    def update(self):
        self.movimiento()

    def movimiento(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.resetear()

    def resetear(self):
        while True:
            new_y = random.randint(50, self.screen.get_height() - 150)
            new_rect = self.image.get_rect(midright=(self.screen.get_width(), new_y))

            # Verificar si hay colisión con otros obstáculos
            collision = False
            for obj in self.objetos:
                if new_rect.colliderect(obj.rect):
                    collision = True
                    break

            if not collision:
                self.rect = new_rect
                break
