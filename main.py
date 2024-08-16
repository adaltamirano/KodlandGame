import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Kodland Game")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)


# Función para dibujar el jugador
def dibujar_jugador(pantalla, x, y):
    pygame.draw.rect(pantalla, AZUL, (x, y, 50, 50))


# Función para dibujar las estrellas
def dibujar_estrella(pantalla, estrella):
    pygame.draw.ellipse(pantalla, AMARILLO, estrella)


# Función principal del juego
def juego():
    reloj = pygame.time.Clock()

    # Coordenadas del jugador
    x_jugador = ANCHO // 2
    y_jugador = ALTO - 60
    velocidad_jugador = 5

    # Lista de estrellas
    estrellas = []
    for _ in range(5):
        x_estrella = random.randint(0, ANCHO - 20)
        y_estrella = random.randint(-300, 0)
        estrellas.append(pygame.Rect(x_estrella, y_estrella, 20, 20))

    puntuacion = 0
    estrellas_perdidas = 0  # Contador de estrellas perdidas
    fuente = pygame.font.Font(None, 36)

    jugando = True
    perdiste = False

    # Bucle principal del juego
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

            # Reiniciar el juego si el jugador ha perdido y presiona la tecla espaciadora
            if perdiste and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    juego()  # Reinicia el juego

        if not perdiste:
            # Movimiento del jugador
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and x_jugador > 0:
                x_jugador -= velocidad_jugador
            if teclas[pygame.K_RIGHT] and x_jugador < ANCHO - 50:
                x_jugador += velocidad_jugador

            # Movimiento de las estrellas
            for estrella in estrellas:
                estrella.y += 3
                if estrella.y > ALTO:
                    estrella.x = random.randint(0, ANCHO - 20)
                    estrella.y = random.randint(-300, 0)
                    estrellas_perdidas += 1  # Incrementa el contador de estrellas perdidas

            # Colisión entre el jugador y las estrellas
            for estrella in estrellas:
                if pygame.Rect(x_jugador, y_jugador, 50, 50).colliderect(estrella):
                    puntuacion += 10
                    estrella.x = random.randint(0, ANCHO - 20)
                    estrella.y = random.randint(-300, 0)

            # Verificar si el jugador ha perdido
            if estrellas_perdidas >= 10:
                perdiste = True

        # Dibujar en pantalla
        pantalla.fill(NEGRO)
        dibujar_jugador(pantalla, x_jugador, y_jugador)
        for estrella in estrellas:
            dibujar_estrella(pantalla, estrella)

        # Mostrar la puntuación
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        pantalla.blit(texto_puntuacion, (10, 10))

        # Mostrar mensaje de "Perdiste" si el jugador ha perdido
        if perdiste:
            texto_perdiste = fuente.render("Perdiste! Presiona ESPACIO para reiniciar", True, ROJO)
            pantalla.blit(texto_perdiste, (ANCHO // 2 - texto_perdiste.get_width() // 2, ALTO // 2))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()


# Función para mostrar el menú
def mostrar_menu():
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_opciones = pygame.font.Font(None, 50)

    titulo = fuente_titulo.render("Kodland Game", True, BLANCO)
    opciones_texto = ["Comenzar juego", "Salir"]
    seleccion = 0

    while True:
        pantalla.fill(NEGRO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))

        for i, texto in enumerate(opciones_texto):
            if i == seleccion:
                opcion = fuente_opciones.render(texto, True, ROJO)  # Cambia de color cuando está seleccionado
            else:
                opcion = fuente_opciones.render(texto, True, BLANCO)
            pantalla.blit(opcion, (ANCHO // 2 - opcion.get_width() // 2, 300 + i * 100))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones_texto)
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones_texto)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:  # Comenzar juego
                        juego()
                    if seleccion == 1:  # Salir
                        pygame.quit()
                        quit()

        pygame.display.flip()


# Llamada a la función para mostrar el menú al inicio
mostrar_menu()
