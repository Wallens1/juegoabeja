import pygame
import os
from nivel import Nivel

# Colores
sky_blue = (0, 210, 255)
ground_color = (0, 128, 0)
button_text_color = (128, 64, 0)

# Rutas de archivos desde la carpeta del juego
script_dir = os.path.dirname(os.path.abspath(__file__))

# Archivos

font_path = os.path.join(script_dir, 'assets/Jaro-Regular-VariableFont_opsz.ttf')
button_path = os.path.join(script_dir, 'assets/imagen_2024-06-06_220829731-removebg-preview.png')
image_above_button_path = os.path.join(script_dir, 'assets/1497109.png')
cloud_image_path = os.path.join(script_dir, 'assets/computacion-en-la-nube (1).png')
bee_image_path = os.path.join(script_dir, 'assets/abejas.png')

class Juego:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()
        self.running = True
        self.vidas_abeja = 3
        pygame.mixer.music.load(os.path.join(script_dir,'assets/musica.wav'))
        pygame.mixer.music.play(-1)

    def iniciar(self):
        
        pygame.font.init()
        self.font = pygame.font.Font(font_path, 70)

        while self.running:
            self.main_screen()

        pygame.quit()

    def main_screen(self):
        button_image = pygame.image.load(button_path)
        button_width, button_height = 300, 175  
        button_image = pygame.transform.scale(button_image, (button_width, button_height))
        button_rect = button_image.get_rect(center=self.screen.get_rect().center)
        second_button_rect = button_rect.copy()
        second_button_rect.top += button_height + 20 

        image_above_button = pygame.image.load(image_above_button_path).convert_alpha()
        image_above_button = pygame.transform.scale(image_above_button, (150, 150))
        image_above_button_rect = image_above_button.get_rect(center=(button_rect.centerx, button_rect.y - 100))

        cloud_positions = [(100, 20), (300, 300), (700, 100), (1000, 300), (1300, 100), (1500, 400)]
        cloud_speed = 3

        show_main_screen = True

        while show_main_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    show_main_screen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and button_rect.collidepoint(event.pos):
                        show_main_screen = False
                        self.second_screen()

            if show_main_screen:
                self.draw_main_screen(button_image, button_rect, second_button_rect, image_above_button, image_above_button_rect, cloud_positions, cloud_speed)
                pygame.display.flip()
                self.clock.tick(60)

        if self.vidas_abeja <= 0:
            self.vidas_abeja = 3  # Reinicia las vidas
        else:
            self.running = False

    def draw_main_screen(self, button_image, button_rect, second_button_rect, image_above_button, image_above_button_rect, cloud_positions, cloud_speed):
        self.screen.fill(sky_blue)
        pygame.draw.rect(self.screen, ground_color, (0, self.screen_height - 50, self.screen_width, 50))

        for i, (x, y) in enumerate(cloud_positions):
            cloud_positions[i] = (self.draw_cloud(x, y, cloud_speed), y)

        self.screen.blit(button_image, button_rect)
        
        self.draw_button_with_text(button_image, "¡JUGAR!", button_text_color, button_rect.topleft)
        self.screen.blit(image_above_button, image_above_button_rect)

        self.draw_text("¡SWEET", (255, 255, 255), (150, 150), 150)
        self.draw_text("FLY!", (255, 255, 255), (1000, 150), 150)

    def draw_cloud(self, x, y, cloud_speed):
        cloud_image = pygame.image.load(cloud_image_path).convert_alpha()
        cloud_resized = pygame.transform.scale(cloud_image, (200, 175))
        cloud_x = x - cloud_speed
        if cloud_x <= -cloud_resized.get_width():
            cloud_x = self.screen_width
        self.screen.blit(cloud_resized, (cloud_x, y))
        return cloud_x

    def draw_text(self, text, color, position, size):
        font = pygame.font.Font(font_path, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_button_with_text(self, image, text, text_color, position):
        font = pygame.font.Font(font_path, 70)
        self.screen.blit(image, position)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(position[0] + image.get_width() // 2, position[1] + image.get_height() // 2))
        self.screen.blit(text_surface, text_rect)

    def second_screen(self):
        nivel = Nivel(self.screen, self.screen_width, self.screen_height, self.vidas_abeja)
        nivel.nivel_1()