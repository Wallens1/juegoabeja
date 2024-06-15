import pygame
from juego import Juego

def main():
    pygame.init()
    screen_width, screen_height = 1500, 770
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Bees")

    menu = Juego(screen, screen_width, screen_height)
    print("Juego inicializado")
    menu.iniciar()
    print("Menú iniciado")

if __name__ == "__main__":
    main()
