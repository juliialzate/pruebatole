import pygame

class Pajaro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.explosion_image = pygame.image.load("imagenes/tiro.png")
        self.explosion_image = pygame.transform.scale(self.explosion_image, (150, 150))  # Ajustar el tamaño de la explosión
        self.rect = self.explosion_image.get_rect()
        self.alive = True
        self.explosion_timer = 0
        self.explosion_duration = 900

    def dibujar_explosion(self, screen, collision_pos):
        # Ajusta la posición en x para mover la explosión un poco más a la derecha
        explosion_x = collision_pos[0] + 20  # Por ejemplo, suma 20 píxeles a la posición x
        # Dibuja la explosión en la posición ajustada
        screen.blit(self.explosion_image, (explosion_x, collision_pos[1]))
        pygame.display.update()  # Actualiza la pantalla para mostrar la explosión


    def is_explosion_finished(self):
        return pygame.time.get_ticks() - self.explosion_timer >= self.explosion_duration  # Verificar si la explosión ha terminado

class Vuelo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.animacion = False
        self.sprites = []
        self.sprites_invertidos = []

        # Cargar y preparar las imágenes normales e invertidas
        for i in range(1, 10):
            sprite = pygame.image.load(f"imagenes/pajaro{i}.png").convert_alpha()
            self.sprites.append(sprite)
            self.sprites_invertidos.append(pygame.transform.flip(sprite, True, False))

        self.sprite_actual = 0
        self.image = self.sprites[self.sprite_actual]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        
        self.direccion = 'derecha'
        self.contador_movimientos = 0
        self.movimientos_totales = 0

    def movimiento(self):
        self.animacion = True

    def volar_derecha(self, speed):
        self.sprite_actual += speed
        if int(self.sprite_actual) >= len(self.sprites):
            self.sprite_actual = 0

        self.rect.x += 2
        self.rect.y -= 7

        if self.rect.right < 0 or self.rect.bottom < 0:
            self.rect.topleft = (self.rect.topleft[0] + 2, 700)

        if self.rect.topleft[0] >= 768:
            self.rect.topleft = (0, 700)

        self.image = self.sprites[int(self.sprite_actual)]

        self.movimientos_totales += 1
        if self.movimientos_totales >= 106:
            self.contador_movimientos += 1
            self.movimientos_totales = 0
            print(f"Se han completado {self.contador_movimientos} ciclos de 116 movimientos hacia la derecha")

    def volar_izquierda(self, speed):
        self.sprite_actual += speed
        if int(self.sprite_actual) >= len(self.sprites):
            self.sprite_actual = 0

        self.rect.x -= 2
        self.rect.y -= 7

        if self.rect.right < 0 or self.rect.bottom < 0:
            self.rect.topleft = (self.rect.topleft[0] - 2, 700)

        if self.rect.topleft[0] < 0:
            self.rect.topleft = (700, 600)

        # Usar las imágenes invertidas
        self.image = self.sprites_invertidos[int(self.sprite_actual)]

        self.movimientos_totales += 1
        if self.movimientos_totales >= 106:
            self.contador_movimientos += 1
            self.movimientos_totales = 0
            print(f"Se han completado {self.contador_movimientos} ciclos de 116 movimientos hacia la izquierda")

    def get_hitbox(self):
        return self.rect.inflate(-10, -10)  # Ajusta el tamaño de la hitbox si es necesario

    def caer(self, speed):
        if self.animacion:
            self.sprite_actual += speed
            if int(self.sprite_actual) >= len(self.sprites):
                self.sprite_actual = 0

            self.rect.x += 1
            self.rect.y += 10

            mouse_pos = pygame.mouse.get_pos()
            if self.get_hitbox().collidepoint(mouse_pos):
                print("Colisión con el mouse detectada")
                # Cambiar posición del pájaro
                self.rect.x += 1
                self.rect.y += 15

            if self.rect.y > 700:
                self.rect.topleft = (0, 500)  # Reubicar en la posición (0, 600)
                self.animacion = False  # Detener la animación temporalmente
                self.volar_derecha(speed)  # Ejecutar el método volar_derecha

            self.image = self.sprites[int(self.sprite_actual)]
        
    def obtener_contador_movimientos(self):
        return self.contador_movimientos

