import pygame
from pajaro import *

class RondasJuego:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.imagenes_rondas = [pygame.image.load(f"imagenes/ronda{i}.png").convert_alpha() for i in range(1, 4)]
        self.imagen_actual = 0
        self.mostrar_imagen = True
        self.tiempo_inicio = pygame.time.get_ticks()
        self.mostrar_primera_imagen = True
        self.rondas_totales = 0  # Contador de rondas totales

    def verificar_reinicio_contador(self):
        if self.vuelo.obtener_contador_movimientos() == 0:
            self.mostrar_imagen = True
            self.tiempo_inicio = pygame.time.get_ticks()
            self.imagen_actual = min(self.imagen_actual + 1, len(self.imagenes_rondas) - 1)
            self.rondas_totales += 1  # Incrementar las rondas totales
            print(f"Rondas totales completadas: {self.rondas_totales}")

    def mostrar_ronda(self, screen):
        if self.mostrar_imagen:
            screen.blit(self.imagenes_rondas[self.imagen_actual], (235, 600))
            if pygame.time.get_ticks() - self.tiempo_inicio > 2000:  # Mostrar la imagen por 2 segundos
                self.mostrar_imagen = False

    def mostrar_primera_ronda(self, screen):
        if self.mostrar_primera_imagen:
            screen.blit(self.imagenes_rondas[0], (235, 600))
            if pygame.time.get_ticks() - self.tiempo_inicio > 2000:  # Mostrar la imagen por 2 segundos
                self.mostrar_primera_imagen = False

    def reiniciar_rondas(self):
        self.imagen_actual = 0
        self.mostrar_imagen = True
        self.tiempo_inicio = pygame.time.get_ticks()
        self.mostrar_primera_imagen = True
        self.rondas_totales = 0  # Reiniciar las rondas totales

    def obtener_rondas_totales(self):
        return self.rondas_totales

    def verificar_y_mostrar_scoref(self, screen, scoref):
        if self.rondas_totales >= 3:
            scoref.mostrar_scoref()
            self.reiniciar_rondas()
            return True
        return False

    def inicializar_tiempo_inicio(self):
        self.tiempo_inicio = pygame.time.get_ticks()