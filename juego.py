import pygame
from ajustes import *
from portada import toleportada
from menu import tolemenu
from fondo import FondoBase, FondoMontañas
from pajaro import *
from shot import Mirilla, handle_crosshair, crosshair_img
from colision import handle_collisions
from decision import toledecision
from creditos import Creditos
from rondas import *
from scoref import Scoref
import sys

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class Juego:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.Tamaño_pantalla = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.Tamaño_pantalla)
        pygame.display.set_caption(titulo)
        self.clock = pygame.time.Clock()
        self.juego_terminado = False
        self.creditos_mostrados = False
        self.start_time = None
        self.num_balas = 5
        self.score = 0
        self.mirilla = None
        self.vuelo = Vuelo(0, 600)
        self.pajaro = Pajaro()
        self.moving_sprites = pygame.sprite.Group(self.vuelo)
        self.font = pygame.font.Font(None, 35)
        self.rondas_juego = RondasJuego(self.vuelo)  # Instancia de RondasJuego
        self.scoref = Scoref(self.screen)  # Instancia de Scoref
        self.creditos = Creditos()  # Instancia de Creditos

        self.balas_img = pygame.image.load("imagenes/bullet.png")
        self.balas_img = pygame.transform.scale(self.balas_img, (30, 30))

        pygame.mixer.music.load("sonidos/oyeme.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def mostrar_contadores(self):
        # Mostrar contador de balas
        for i in range(self.num_balas):
            self.screen.blit(self.balas_img, (52 + i * 30, 68))

        # Mostrar contador de puntaje
        score_texto = f"{self.score}"
        score_renderizado = self.font.render(score_texto, True, YELLOW)  # Cambiar el color a amarillo
        self.screen.blit(score_renderizado, (620, 70))

    def mostrar_creditos(self):
        self.screen.blit(self.creditos, (0, 0))
        pygame.display.flip()
        self.creditos_mostrados = True

    def handle_shooting(self, event):
        global can_shoot, last_shot_time
        current_time = pygame.time.get_ticks()
        if self.num_balas > 0:
            if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
                can_shoot = False
                last_shot_time = current_time
                print("Disparo registrado")
                mouse_pos = event.pos
                collision_pos = None
                if self.num_balas > 0:
                    self.num_balas, self.score, collision_pos = handle_collisions(self.vuelo, self.mirilla, self.num_balas, self.score, mouse_pos)
                if collision_pos is not None:
                    self.reproducir_sonido_colision()
                    self.pajaro.dibujar_explosion(self.screen, collision_pos)
                    self.scoref.actualizar_score(self.score)
                    self.pajaro.alive = False
                else:
                    self.reproducir_sonido_fallido()
                    self.num_balas -= 1

                self.mirilla.shoot()

        if current_time - last_shot_time > 1500:
            can_shoot = True

    def mostrar_imagenes(self):
        self.rondas_juego.mostrar_ronda(self.screen)

        if self.vuelo.obtener_contador_movimientos() == 4:
            print("Se ha completado una ronda. Reiniciando contador.")
            self.vuelo.contador_movimientos = 0
            self.rondas_juego.verificar_reinicio_contador()

    def reiniciar_pajaro(self):
        if not self.vuelo.alive:
            print("Reiniciando el pájaro para una nueva ronda")
            self.vuelo.rect.topleft = (0, 600)
            self.vuelo.alive = True
            self.pajaro.explosion_frames = 0
            self.vuelo.movimiento()

    def reproducir_sonido_colision(self):
        pygame.mixer.Sound("sonidos/pollo.mp3").play()

    def reproducir_sonido_fallido(self):
        pygame.mixer.Sound("sonidos/disparo.mp3").play()

    def run(self):
        mostrar_portada = toleportada(2)

        if mostrar_portada:
            iniciar_juego = tolemenu()

            if iniciar_juego:
                print("sisas")

                fondo = FondoBase()
                montañas = FondoMontañas()

                self.mirilla = Mirilla(crosshair_img)
                self.vuelo.movimiento()

                global can_shoot, last_shot_time
                can_shoot = True
                last_shot_time = 0

                self.rondas_juego.inicializar_tiempo_inicio()

                self.start_time = pygame.time.get_ticks()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        self.handle_shooting(event)

                    if self.juego_terminado:
                        if not self.creditos_mostrados:
                            decision = toledecision()
                            if decision == "continuar":
                                self.juego_terminado = False
                                self.start_time = pygame.time.get_ticks()
                            elif decision == "creditos":
                                creditos = Creditos()
                                self.creditos.mostrar_creditos()
                                pygame.time.wait(5000)
                                pygame.quit()
                                sys.exit()
                    else:
                        self.screen.fill(WHITE)
                        self.screen.blit(fondo.image, fondo.rect)

                        # Alternar entre volar_derecha y volar_izquierda cada 3 movimientos
                        if (self.vuelo.contador_movimientos // 3) % 2 == 0:
                            self.vuelo.volar_derecha(0.50)
                            print("derecha")
                        else:
                            self.vuelo.volar_izquierda(0.50)
                            print("izquierda")

                        mouse_pos = pygame.mouse.get_pos()
                        handle_crosshair(self.num_balas, self.mirilla, self.screen)

                        if not self.vuelo.alive:
                            print("El pajaro ha sido derribado")
                            self.num_balas, self.score, collision_pos = handle_collisions(self.vuelo, self.mirilla, self.num_balas, self.score, mouse_pos)
                            if collision_pos is not None:
                                self.pajaro.dibujar_explosion(self.screen, collision_pos)

                            if self.pajaro.is_explosion_finished():
                                self.reiniciar_pajaro()

                        self.mostrar_contadores()

                        self.moving_sprites.draw(self.screen)
                        self.moving_sprites.update(0.40)

                        self.screen.blit(montañas.image, montañas.rect)
                        self.rondas_juego.mostrar_primera_ronda(self.screen)

                        texto = f"{self.vuelo.contador_movimientos}/3"
                        texto_renderizado = self.font.render(texto, True, (255, 255, 255))
                        self.screen.blit(texto_renderizado, (365, 70))

                        self.mostrar_imagenes()

                        if self.rondas_juego.verificar_y_mostrar_scoref(self.screen, self.scoref):
                            self.scoref.score = self.score
                            self.scoref.mostrar_scoref()
                            pygame.time.wait(4000)
                            decision = toledecision()
                            if decision == "continuar":
                                self.juego_terminado = False
                                self.start_time = pygame.time.get_ticks()
                            elif decision == "creditos":
                                self.creditos.mostrar_creditos()
                                pygame.time.wait(6000)
                                pygame.quit()
                                sys.exit()

                        pygame.display.update()

                    self.clock.tick(60)

                    if self.vuelo.obtener_contador_movimientos() == 4:
                        print("Se ha completado una ronda. Reiniciando contador y rondas.")
                        self.vuelo.contador_movimientos = 0
                        self.rondas_juego.reiniciar_rondas()

if __name__ == "__main__":
    juego = Juego()
