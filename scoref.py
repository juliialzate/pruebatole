# En scoref.py
import pygame
from ajustes import *

class Scoref:
    def __init__(self, screen):
        self.screen = screen
        self.scoref_mostrados = False
        self.font = pygame.font.Font(None, 70)  
        self.score = 0  

    def mostrar_scoref(self):
        scoref = pygame.image.load('imagenes/scoref.jpg')
        self.screen.blit(scoref, (0, 0))

        
        score_text = f"{self.score}"
        score_renderizado = self.font.render(score_text, True, (255, 255, 0))  # Color blanco

        
        self.screen.blit(score_renderizado, (330, 435))

        pygame.display.flip()
        self.scoref_mostrados = True

    def actualizar_score(self, nuevo_score):
        self.score = nuevo_score
