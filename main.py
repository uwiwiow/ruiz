import pygame
import sys
from pygame import mixer
import fighter
from button import Button
import os
import json

mixer.init()
pygame.init()

global all_round_damage1
all_round_damage1 = 0
global all_round_damage2
all_round_damage2 = 0

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [1, 1]  # numeros rojos == vidas
score_d = [0, 0]  # player scores. [P1, P2]     numeros amarillos == kills
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
scoredm_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
arial = pygame.font.SysFont("Arial", 24)


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


def save_data(data):
    if not os.path.exists("data"):
        # Si el directorio no existe, crearlo
        os.makedirs("data")

    if os.path.exists("data/score.txt"):

        with open("data/score.txt", 'r') as f:
            datas = json.load(f)

        if data[2] > datas[2]:
            with open("data/score.txt", 'w') as f:
                json.dump(data, f)

        if os.path.exists("data/all_scores.txt"):
            with open("data/all_scores.txt", 'r') as f:
                all_scores = json.load(f)

            all_scores.extend(data)

            with open("data/all_scores.txt", 'w') as f:
                json.dump(all_scores, f)

        else:
            with open("data/all_scores.txt", 'w') as f:
                json.dump(data, f)

    else:
        with open("data/score.txt", 'w') as f:
            json.dump(data, f)

        if os.path.exists("data/all_scores.txt"):
            with open("data/all_scores.txt", 'r') as f:
                all_scores = json.load(f)

            all_scores.extend(data)

            with open("data/all_scores.txt", 'w') as f:
                json.dump(all_scores, f)

        else:
            with open("data/all_scores.txt", 'w') as f:
                json.dump(data, f)


# create two instances of fighters
fighter_1 = fighter.Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = fighter.Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

run = True


def end_session():
    base_font = pygame.font.Font("assets/fonts/turok.ttf", 48)
    user_text = ''

    # create rectangle
    input_rect = pygame.Rect((SCREEN_WIDTH // 2) - 50, 300, 140, 48)

    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')

    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('grey')
    active = False
    background_img = pygame.image.load('assets/images/background/credits.jpg').convert_alpha()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    if os.path.exists("data/score.txt"):

        with open("data/score.txt", 'r') as f:
            recent_score = json.load(f)

        is_score = True
    else:
        is_score = False

    while True:
        screen.blit(background_img, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        font = pygame.font.Font("assets/fonts/turok.ttf", 60)

        menu_text = font.render("El ganador es " + ganador, True, "#AAAA00")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(menu_text, menu_rect)

        win_text = font.render("Por favor ingrese su nombre", True, "#AAAA00")
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(win_text, win_rect)

        sc_text = score_font.render("Mayor score registrado", True, "#1C9D93")
        sc_rect = sc_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(sc_text, sc_rect)

        if is_score:
            last_text = score_font.render(
                "Nombre: " + str(recent_score[0]) + "   Kills: " + str(recent_score[1]) + "    Damage total: " + str(recent_score[2]), True, "#60e1d7")
            last_rect = last_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
            screen.blit(last_text, last_rect)

        play_button = Button(image=None, pos=(SCREEN_WIDTH // 2, 400),
                             text_input="Save", font=font, base_color='grey', hovering_color='lightskyblue3')

        play_button.change_color(mouse_pos)
        play_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if play_button.check_for_input(mouse_pos):
                    if ganador == "Jugador 2":
                        kills = score_d[1]
                        damages = all_round_damage2

                    else:
                        kills = score_d[0]
                        damages = all_round_damage1


                    data = [user_text, kills, damages]
                    save_data(data)
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:

                    user_text = user_text[:-1]

                else:
                    user_text += event.unicode

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        screen.blit(text_surface, (input_rect.x + 5, input_rect.y - 7))

        input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.display.flip()


while run:

    clock.tick(FPS)

    draw_bg()

    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text('score:' + str(score_d[0]), scoredm_font, YELLOW, 20, 80)
    draw_text('movimiento: w s a d', scoredm_font, "#555555", 20, 100)
    draw_text('atk: r - t', scoredm_font, "#555555", 20, 120)

    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
    draw_text('score:' + str(score_d[1]), scoredm_font, YELLOW, 580, 80)
    draw_text('movimiento: ', scoredm_font, "#555555", 580, 100)
    draw_text('↑ ↓ ← →', arial, "#555555", 750, 105)
    draw_text('atk: o - p', scoredm_font, "#555555", 580, 120)
    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    fighter.damage_text_group.update()
    fighter.damage_text_group.draw(screen)

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # print(fighter_1.health)

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    global ganador

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            # gana el mago

            damage2 = fighter_2.total_damage
            all_round_damage2 += damage2
            score[0] -= 1
            score_d[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            # gana el guerrero

            damage1 = fighter_1.total_damage
            all_round_damage1 += damage1
            score[1] -= 1
            score_d[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            if score[0] == 0 or score[1] == 0:
                if score[0] == 0:
                    ganador = "Jugador 2"
                if score[1] == 0:
                    ganador = "Jugador 1"
                end_session()
            round_over = False
            intro_count = 3
            fighter_1 = fighter.Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                        sword_fx)
            fighter_2 = fighter.Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    # update display
    pygame.display.update()

# exit pygame
pygame.quit()
