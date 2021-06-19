import json
import pygame
pygame.init()

flatten = lambda l: [item for sublist in l for item in sublist]

with open("data.json", "r") as file:
    data = json.load(file)

original_deaths = [death["cause"] for death in flatten([hc["deaths"] for hc in data["hardcores"]])]
total_deaths = len(original_deaths)

deaths = flatten(original_deaths)
death_type = []
death_count = []
death_percent = []

for death in deaths:
    if death not in death_type:
        death_type.append(death)
        death_count.append(1)
    else:
        death_count[death_type.index(death)] += 1

death_percent = [count / total_deaths for count in death_count]

final_list = list(zip(death_type, death_count, death_percent))

stat_quant = len(death_type)
HEIGHT = 200 + (100 * stat_quant)
WIDTH = 700
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.Surface(SCREEN_SIZE)
running = True

# // Images
topbar = pygame.image.load("stats/topbar.png")
stonebricks = pygame.image.load("stats/stonebricks.png")
prog_bg = pygame.image.load("stats/progress_bg.png")
prog = pygame.image.load("stats/progress.png")


screen.fill((0, 0, 0))
for idx, i in enumerate(sorted(final_list, key=lambda x: x[1], reverse=True)):
    text = pygame.font.SysFont("Arial", 32, bold=True).render(i[0] + " (" + str(i[1]) + ")", False, (255, 255, 255))
    text2 = pygame.font.SysFont("Arial", 26).render(str(round(i[2] * 100, 2)) + "%", False, (255, 255, 255))
    screen.blit(stonebricks, (0, 200 + (idx * 100)))
    screen.blit(prog_bg, (20, 250 + (idx * 100)))
    screen.blit(text, text.get_rect(center=(300, 235 + (idx * 100))))
    screen.blit(pygame.transform.scale(prog, (int(i[2] * 585), 28)), (26, 250 + (idx * 100)))
    screen.blit(text2, (610, 250 + (idx * 100)))

screen.blit(topbar, (0, 0))

pygame.image.save(screen, "output/deathpercent.png")
