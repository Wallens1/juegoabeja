import pygame
import os

# Rutas de archivos desde la carpeta del juego
script_dir = os.path.dirname(os.path.abspath(__file__))
image_above_button_path = os.path.join(script_dir, 'assets/1497109.png')

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(image_above_button_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 15  # Velocidad de movimiento del jugador

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.rect.y = max(self.rect.y, 0)
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.rect.y = min(self.rect.y, 770 - self.rect.height)  # Ajusta el límite inferior según la altura de la pantalla
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.rect.x = max(self.rect.x, 0)
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.rect.x = min(self.rect.x, 500 - self.rect.width)  # Ajusta el límite derecho según el ancho de la pantalla

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reiniciar_posicion(self, x, y):
        self.rect.topleft = (x, y)
