import pygame
import sys
import random
import os
import time
from jugador import Jugador
from obstaculo import ObstaculoStatic

pygame.init()
script_dir = os.path.dirname(os.path.abspath(__file__))

#sonidos
golpe = pygame.mixer.Sound(os.path.join(script_dir,'assets/golpe.wav'))
muerte = pygame.mixer.Sound(os.path.join(script_dir,'assets/muerte.wav'))

#colores
sky_blue = (0, 210, 255)
ground_color = (0, 128, 0)
button_text_color = (128, 64, 0)
pygame.init()

#rutas de archivos
font_path = os.path.join(script_dir, 'assets/Jaro-Regular-VariableFont_opsz.ttf')
score_image_path = os.path.join(script_dir, 'assets/image-removebg-preview (2).png')
bee_image_path = os.path.join(script_dir,'assets/abejas.png')
button_path = os.path.join(script_dir,'assets','imagen_2024-06-06_220829731-removebg-preview.png')


class Nivel:
    def __init__(self, screen, screen_width, screen_height, vidas_abeja):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()
        self.vidas_abeja = vidas_abeja
        self.objetos = []  #objetos
        for _ in range(3):
            self.objetos.append(ObstaculoStatic(self.screen, self.objetos))
        self.jugador = Jugador(100, 300)  #pos inicio
        self.colision = False  #colision
        self.score = 0
        self.running = True
        self.abeja_moviendose = True  #movimiento abeja
        self.objetos_moviendo = True  #movimiento objetos
        self.vidas_surface = pygame.Surface((200, 50), pygame.SRCALPHA)

    def nivel_1(self):
        contador = self.contador_score(2, 0.1)
        score_final = 0
        running = True
        score_paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(sky_blue)  #cielo
            pygame.draw.rect(self.screen, (ground_color), (0, self.screen_height - 50, self.screen_width, 50))  #suelo

            if not score_paused:  
                velocidad_actual = next(contador)
                velocidad_int = int(velocidad_actual)
                self.score += velocidad_int  #aumenta el score con la velocidad

            velocidad_str = "{}".format(velocidad_int)
            text_width = len(velocidad_str) * 30
            text_position = (self.screen_width - text_width - 75, 10)
            self.draw_text(velocidad_str, (255, 255, 255), text_position, 50)

            self.mostrar_vidas(self.vidas_abeja)

            #score a la izquierda
            image_score = pygame.image.load(score_image_path).convert_alpha()
            score_resized = pygame.transform.scale(image_score, (75, 50))
            self.screen.blit(score_resized, (1415, 15))

            #muestra al jugador moviendose
            if self.abeja_moviendose:
                self.jugador.update()  # Actualiza el movimiento del jugador
                self.jugador.draw(self.screen)  # Dibuja al jugador en la pantalla


            #linea roja
            pygame.draw.line(self.screen, (255, 0, 0), (self.screen.get_width() - 1000, 0), (self.screen.get_width() - 1000, self.screen.get_height()), 3)

            colision_detectada = False

            #mover y dibujar objetos
            for obj in self.objetos:
                if not score_paused:  #mover si no hay pausa
                    obj.movimiento()
                self.screen.blit(obj.image, obj.rect)

                #detectar colision con jugador
                if obj.rect.colliderect(self.jugador.rect):
                    colision_detectada = True
                    pygame.mixer.Sound.play(golpe)
                    obj.resetear()

            #manejar colisión detectada
            if colision_detectada:
                self.vidas_abeja -= 1
                self.colision = True


            #mostrar pantalla de Game Over
            if self.vidas_abeja <= 0:
                self.mostrar_vidas(0)
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(muerte)
                pygame.time.wait(1000) 
                
                #pausar juego
                score_paused = True
                self.abeja_moviendose = False  #detiene el movimiento de la abeja
                self.objetos_moviendo = False  #detiene el movimiento de los objetos
                self.mostrar_game_over()

                #para reintentar o volver al menú
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()

                            #Clic en reintentar
                            retry_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 30, 200, 50)
                            if retry_button_rect.collidepoint(mouse_pos):
                                print("Reintentar clickeado")
                                pygame.mixer.music.play(-1)
                                self.reintentar_nivel()

                            #clic en el botón  Menú Principal
                            menu_button_rect = pygame.Rect(self.screen_width // 2 - 200, self.screen_height // 2 + 100, 400, 50)
                            if menu_button_rect.collidepoint(mouse_pos):
                                print("Volver al Menú Principal clickeado")
                                self.volver_menu_principal()

                    pygame.display.flip()
                    self.clock.tick(60)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
    
    def contador_score(self, velocidad_inicial, aceleracion_inicial):
        tiempo_inicio = time.time()
        tiempo_transcurrido = 0
        velocidad_actual = velocidad_inicial
        aceleracion_actual = aceleracion_inicial

        while True:
            tiempo_actual = time.time()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio  

            aceleracion_actual = aceleracion_inicial + tiempo_transcurrido * 0.0001
            velocidad_actual += aceleracion_actual

            yield velocidad_actual

    def draw_text(self, text, color, position, size):
        font = pygame.font.Font(font_path, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def mostrar_vidas(self, cantidad_vidas):
        self.vidas_surface.fill((sky_blue))
        if cantidad_vidas > 0:
            vidas_image = pygame.image.load(bee_image_path).convert_alpha()
            vidas_resized = pygame.transform.scale(vidas_image, (50, 50))
            x = 0
            y = 0
            for i in range(cantidad_vidas):
                self.vidas_surface.blit(vidas_resized, (x, y))
                x += vidas_resized.get_width() + 10

        self.screen.blit(self.vidas_surface, (20, 20))

    def draw_rounded_rect(self, surface, rect, color, radius):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def reintentar_nivel(self):
        self.vidas_abeja = 3
        self.score = 0
        self.jugador.reiniciar_posicion(100,300)
        self.abeja_moviendose = True
        self.objetos_moviendo = True
        pygame.mixer.music.load(os.path.join(script_dir,'assets/musica.wav'))
        pygame.mixer.music.play(-1)
        self.nivel_1()

    def draw_button_with_text(self, image, text, text_color, position):
        font = pygame.font.Font(font_path, 30)
        self.screen.blit(image, position)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(position[0] + image.get_width() // 2, position[1] + image.get_height() // 2))
        self.screen.blit(text_surface, text_rect)

    def mostrar_game_over(self):

        #crear fuente y renderizar texto
        game_over_font = pygame.font.Font(font_path, 100)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, (self.screen_height // 2) - 150))

        #cuadro con esquinas redondeadas
        rect_width = 600
        rect_height = 400
        rect_x = self.screen_width // 2 - rect_width // 2
        rect_y = self.screen_height // 2 - rect_height // 2
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        radius = 20

        button_width, button_height = 200, 125
        button_image = pygame.image.load(button_path).convert_alpha()
        button_image = pygame.transform.scale(button_image, (button_width, button_height))
        button_position_retry = (self.screen_width // 2 - button_image.get_width() // 2, self.screen_height // 2 - 100)
        button_position_main = (self.screen_width // 2 - button_image.get_width() // 2, self.screen_height // 2 + 30)

        self.draw_rounded_rect(self.screen, rect, button_text_color, radius)

        self.draw_button_with_text(button_image, "Reintentar", button_text_color, button_position_retry)
        self.draw_button_with_text(button_image, "Salir", button_text_color, button_position_main)

        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        #eventos para los botones
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()

                        #Reintentar
                        if pygame.Rect(button_position_retry[0], button_position_retry[1], button_image.get_width(), button_image.get_height()).collidepoint(mouse_pos):
                            self.reintentar_nivel()

                        #Salir
                        elif pygame.Rect(button_position_main[0], button_position_main[1], button_image.get_width(), button_image.get_height()).collidepoint(mouse_pos):
                            self.volver_menu_principal()
                            return

            pygame.display.flip()
            self.clock.tick(60)