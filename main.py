import pygame
import json
import cv2 as cv
import random
import numpy as np

pygame.init()


def get_arial(size):
    return pygame.font.SysFont("Arial", size, bold=True)


def get_dragoncaps(size):
    return pygame.font.Font("dragoncaps.ttf", size)


def get_grayscale(surface):
    nparr = pygame.surfarray.array3d(surface)

    avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in nparr]
    arr = np.array([[[avg, avg, avg] for avg in col] for col in avgs])

    return pygame.surfarray.make_surface(arr)


# Main window
SCREEN_SIZE = (1000, 400)
HEIGHT = SCREEN_SIZE[1]
WIDTH = SCREEN_SIZE[0]
screen = pygame.Surface(SCREEN_SIZE)

# Loads hardcore data
with open("data.json", "r") as file:
    data = json.load(file)

# Which hardcore data to parse as an image
current_hc_idx = int(input("Which hardcore would you like to load? " + str(tuple(range(len(data["hardcores"])))) + " "))

hc = data["hardcores"][current_hc_idx]

players = hc["players"]
deaths = hc["deaths"]
player_qnt = len(players)
dead_players = [death["player"] for death in deaths]

# Loads images
bg_img = pygame.image.load("bg.png")
redx = pygame.image.load("redx.png")

# >> Player Images
player_images = {"Sam": pygame.image.load("player_images/sam.png"),
                 "Seal": pygame.image.load("player_images/seal.png"),
                 "Konrad": pygame.image.load("player_images/konrad.png"),
                 "Alex": pygame.image.load("player_images/alex.png"),
                 "Omar": pygame.image.load("player_images/omar.png"),
                 "Googie": pygame.image.load("player_images/googie.png"),
                 "Diamond": pygame.image.load("player_images/diamond.png")}

death_images = {"fall": pygame.image.load("death_images/fall.png"),
                "creeper": pygame.image.load("death_images/creeper.png"),
                "phantom": pygame.image.load("death_images/phantom.png"),
                "tnt": pygame.image.load("death_images/tnt.png"),
                "lava": pygame.image.load("death_images/lava.png"),
                "vindicator": pygame.image.load("death_images/vindicator.png"),
                "vex": pygame.image.load("death_images/vex.png"),
                "suffocation": pygame.image.load("death_images/suffocation.png"),
                "burn": pygame.image.load("death_images/burn.png"),
                "witherskeleton": pygame.image.load("death_images/witherskeleton.png"),
                "void": pygame.image.load("death_images/void.png"),
                "endermite": pygame.image.load("death_images/endermite.png")}

space_per_player = WIDTH / player_qnt

margin = space_per_player * 0.03
image_size = space_per_player - (margin * 2)

if image_size > 90:
    image_size = 90
    margin = (space_per_player - 90) / 2


screen.fill((100, 10, 10))

screen.blit(bg_img, (0, 0))

title = get_dragoncaps(34).render("Hardcore #" + str(current_hc_idx + 1), False, (0, 0, 0))
screen.blit(title, title.get_rect(center=(SCREEN_SIZE[0] / 2, 45)))

for idx in range(player_qnt):
    surf = pygame.Surface((image_size, image_size))
    img = None

    # Gets player image from dict, excepts if key doesnt exist
    try:
        img = player_images[players[idx]]
    except KeyError:
        img = None

    # Draws profile cover
    if img is not None:
        surf.blit(pygame.transform.scale(img, (int(image_size), int(image_size))), (0, 0))
    else:
        pygame.draw.circle(surf, [random.randint(0, 255) for x in range(3)], [int(image_size / 2) for x in range(2)], int(image_size / 2))

    screen.blit(surf if not players[idx] in dead_players else get_grayscale(surf), (idx * space_per_player + margin, 130))

    if players[idx] in dead_players:
        # Blit red X
        newx = pygame.transform.scale(redx, [int(image_size * 1.2) for x in range(2)])
        screen.blit(newx, newx.get_rect(center=(idx * space_per_player + margin + image_size / 2, 130 + image_size / 2)))

        # Blits death cause image/s
        cause = [death["cause"] for death in deaths if death["player"] == players[idx]][0]
        BOTTOM_HEIGHT = 100
        if len(cause) == 1:
            img_size = 95
        else:
            img_size = BOTTOM_HEIGHT / len(cause) * 1.2

        for idx2 in range(len(cause)):
            death_img = pygame.transform.scale(death_images[cause[idx2]], [int(img_size) for x in range(2)])
            screen.blit(death_img, death_img.get_rect(center=(idx * space_per_player + margin + image_size / 2, 290 + img_size / 2 + idx2 * (BOTTOM_HEIGHT / len(cause)))))

        # Blits death order
        order = [deaths.index(death) + 1 for death in deaths if death["player"] == players[idx]][0]
        num_text = get_arial(25).render(str(order), False, (255, 255, 255))
        screen.blit(num_text, num_text.get_rect(center=(idx * space_per_player + margin + image_size / 2, 260)))

    # Blit Text
    rendered_text = get_arial(20).render(players[idx], False, (255, 255, 255))
    screen.blit(rendered_text, rendered_text.get_rect(center=(idx * space_per_player + space_per_player / 2, 230)))

pygame.image.save(screen, "output/Hardcore" + str(current_hc_idx + 1) + ".png")
