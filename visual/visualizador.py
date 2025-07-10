import pygame
import random

WIDTH, HEIGHT = 800, 600
VELOCIDAD = 2

PISTA_COORDS = (WIDTH // 2 - 30, HEIGHT // 2 + 100)
TORRE_COORDS = (WIDTH // 2 - 30, HEIGHT // 2 + 40)

AVION_POSICIONES = {}
AVION_DESTINOS = {}

def mover_hacia(pos, destino):
    dx = destino[0] - pos[0]
    dy = destino[1] - pos[1]
    dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
    pos[0] += VELOCIDAD * dx / dist
    pos[1] += VELOCIDAD * dy / dist
    return pos

def iniciar_visualizacion(estado_agentes):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Aviones")
    font = pygame.font.SysFont("Courier", 24)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((10, 10, 30))

        screen.blit(font.render("t", True, (255, 255, 0)), TORRE_COORDS)
        screen.blit(font.render("p", True, (150, 255, 150)), PISTA_COORDS)

        eliminar = []

        for agente, estado in list(estado_agentes.items()):
            if "torre" in agente:
                continue

            nombre = agente.split("@")[0].replace("avion", "a")

            if agente not in AVION_POSICIONES:
                AVION_POSICIONES[agente] = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200)]

            if estado == "Aterrizando":
                AVION_DESTINOS[agente] = list(PISTA_COORDS)
            elif agente not in AVION_DESTINOS or estado == "Volando":
                if random.random() < 0.01:
                    AVION_DESTINOS[agente] = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200)]

            pos = AVION_POSICIONES[agente]
            destino = AVION_DESTINOS.get(agente, pos)
            pos = mover_hacia(pos, destino)
            AVION_POSICIONES[agente] = pos

            if estado == "Aterrizando" and abs(pos[0] - PISTA_COORDS[0]) < 5 and abs(pos[1] - PISTA_COORDS[1]) < 5:
                eliminar.append(agente)
                continue

            color = {
                "Volando": (100, 200, 255),
                "Solicita aterrizaje": (255, 255, 0),
                "Esperando": (255, 150, 0),
                "Aterrizando": (0, 255, 0)
            }.get(estado, (180, 180, 180))

            txt = font.render(nombre, True, color)
            screen.blit(txt, pos)

        for agente in eliminar:
            estado_agentes.pop(agente, None)
            AVION_POSICIONES.pop(agente, None)
            AVION_DESTINOS.pop(agente, None)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
