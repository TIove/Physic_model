import pygame

WIDTH = 720
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

RECT_HEIGHT = 50
RECT_WIDTH = 100
RECT_1X = 0 + RECT_WIDTH
RECT_1Y = HEIGHT // 2
RECT_2X = WIDTH // 2 + RECT_WIDTH
RECT_2Y = HEIGHT // 2

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics")
clock = pygame.time.Clock()

stage_1 = True
stage_2 = False

speed_1 = 3.
speed_2 = -1.
mass_1 = 200.
mass_2 = 20.
mu = 0.5  # коэффициент трения скольжения
mode = True # Упругий удар (true) не упругий удар (false)

font = pygame.font.Font(None, 36)
speed1_after1 = 0
speed2_after1 = 0
speed1_after2 = 0
speed2_after2 = 0

counter = 0

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (RECT_1X, RECT_1Y, RECT_WIDTH, RECT_HEIGHT))
    pygame.draw.rect(screen, RED, (RECT_2X, RECT_2Y, RECT_WIDTH, RECT_HEIGHT))

    text_U1 = font.render('U1 = ' + str(round(speed_1, 2)), True, BLACK)
    text_U2 = font.render('U2 = ' + str(round(speed_2, 2)), True, BLACK)
    text_m1 = font.render('m1 = ' + str(mass_1), True, BLACK)
    text_m2 = font.render('m2 = ' + str(mass_2), True, BLACK)
    screen.blit(text_U1, (WIDTH // 4 - 50, 20))
    screen.blit(text_U2, (WIDTH * 3 // 4 - 50, 20))
    screen.blit(text_m1, (WIDTH // 4 - 50, 50))
    screen.blit(text_m2, (WIDTH * 3 // 4 - 50, 50))

    pygame.display.update()

    # Вычисления
    if stage_1:
        speed_1 = max(speed_1 - mu * 10 / FPS / 100, 0)
        if speed_2 < 0:
            speed_2 = speed_2 + mu * 10 / FPS / 100
        else:
            speed_2 = max(speed_2 - mu * 10 / FPS / 100, 0)
        if RECT_1X + speed_1 <= RECT_2X - RECT_WIDTH:
            RECT_1X += speed_1
        elif RECT_1X + RECT_WIDTH < RECT_2X:
            RECT_1X = RECT_2X - RECT_WIDTH
        else:
            speed1_after1 = speed_1
            speed2_after1 = speed_2

            if not mode:
                speed_1 = (mass_1 * speed_1 + mass_2 * speed_2) / (mass_1 + mass_2)
                speed_2 = speed_1
            else:
                buf = speed_1
                speed_1 = ((mass_1 - mass_2) * speed_1 + 2 * mass_2 * speed_2) / (mass_1 + mass_2)
                speed_2 = ((mass_2 - mass_1) * speed_2 + 2 * mass_1 * buf) / (mass_1 + mass_2)
            stage_1 = False
            stage_2 = True

        if RECT_2X + speed_2 >= RECT_1X + RECT_WIDTH:
            RECT_2X += speed_2

    elif stage_2:
        text = font.render('U01 = ' + str(round(speed1_after1, 2)), True, BLACK)
        screen.blit(text, (WIDTH // 4 - 50, 350))
        text = font.render('U02 = ' + str(round(speed2_after1, 2)), True, BLACK)
        screen.blit(text, (WIDTH * 3 // 4 - 50, 350))
        counter += 1
        if speed_1 <= 0:
            speed_1 = min(speed_1 + mu * 10 / FPS / 100, 0)
        else:
            speed_1 = speed_1 - mu * 10 / FPS / 100

        if speed_2 <= 0:
            speed_2 = min(speed_2 + mu * 10 / FPS / 100, 0)
        else:
            speed_2 = speed_2 - mu * 10 / FPS / 100
        if counter == 1:
            speed1_after2 = speed_1
            speed2_after2 = speed_2
            text11 = font.render('U11 = ' + str(round(speed1_after2, 2)), True, BLACK)
            text12 = font.render('U12 = ' + str(round(speed2_after2, 2)), True, BLACK)

        screen.blit(text11, (WIDTH // 4 - 50, 450))

        screen.blit(text12, (WIDTH * 3 // 4 - 50, 450))

        RECT_1X += speed_1
        RECT_2X += speed_2
    pygame.display.flip()

pygame.quit()
