#Using code division template from https://www.youtube.com/watch?v=i6xMBig-pP4

'''
A basic game wherein you navigate a rectangle around in zero-gravity,
avoiding the black hole, while trying to collide with the white hole.
Used to teach my students the basics of pygame.
'''

import pygame
import numpy as np

pygame.init()

#Screen dimensions:
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

#Randomly generate white and black hole coords.
def gen_hole_coords(r):
    return np.random.randint(r, np.min((SCREEN_HEIGHT, SCREEN_WIDTH)) - r, 4)

'''
Since these coords might result in the holes overlapping,
we use this wrapper function to make sure that doesn't happen.
'''
def get_hole_coords(r):
    while True:
        bh_x, bh_y, wh_x, wh_y = gen_hole_coords(r)
        bh_rect = pygame.draw.circle(win,(0,0,0),(bh_x,bh_y),r)
        wh_rect = pygame.draw.circle(win, (255, 255, 255), (wh_x, wh_y), r)
        overlap = bh_rect.colliderect(wh_rect) or bh_rect.colliderect(player)
        if not overlap:
            return bh_x, bh_y, wh_x, wh_y

#Init display!
win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#Load the background spacey image.
background_image = pygame.image.load("assets/space.jpeg").convert()

#Shout out to Wheatley and the Space Core.
pygame.display.set_caption('SPACE!!!')

#Player dimensions. You are a rectangle. Deal with it.
x = 50
y = 50
w = 40
h = 60
#Player velocity vector (yay space!)
vel = [0,0]
#The rate at which controls change components of the velocity vector.
#I.e. acceleration.
dv = .5
#The braking coefficient.
dampener = 0.9

#Ready Player One.
player = pygame.Rect((x, y, w, h))

#Coords for black and white holes:
r = 60
bh_x, bh_y, wh_x, wh_y = get_hole_coords(r)
#Init draw for the holes.
bh_rect = pygame.draw.circle(win, (0, 0, 0), (bh_x, bh_y), r)
wh_rect = pygame.draw.circle(win, (255, 255, 255), (wh_x, wh_y), r)

#Init score.
points = 0

#Some basic color constants.
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

#A basic font for the score board.
font = pygame.font.Font('freesansbold.ttf', 32)


# --- mainloop ---

run = True
#Unorthodox way of counting frames.
frames = 0

while run:

    # --- events ---
    pygame.time.delay(10)
    for event in pygame.event.get():

        # --- global events ---
        if event.type == pygame.QUIT:
            run = False

    # --- objects events ---
    keys = pygame.key.get_pressed()

    #Navigation setup.
    if keys[pygame.K_LEFT]:
        vel[0] -= dv
    if keys[pygame.K_RIGHT]:
        vel[0] += dv
    if keys[pygame.K_UP]:
        vel[1] -= dv
    if keys[pygame.K_DOWN]:
        vel[1] += dv
    if keys[pygame.K_b]:
        vel=[v*dampener for v in vel]
    if keys[pygame.K_SPACE]:
        player.x = (SCREEN_WIDTH/2)-w
        player.y = (SCREEN_HEIGHT/2)-h
        vel = [0,0]

    # --- updates ---
    #Update position by the components of the velocity vector.
    player.x += vel[0]
    player.y += vel[1]

    #Bounce off the screen edges.
    if player.x < 0 or player.x > SCREEN_WIDTH-w:
        vel[0] = -1*vel[0]
    if player.y < 0 or player.y > SCREEN_HEIGHT-h:
        vel[1] = -1*vel[1]

    #Kill the game if you run into the black hole:
    if player.colliderect(bh_rect):
        run = False
    #Increase points if you run into the white hole,
    #also, pick new locations for the holes.
    if player.colliderect(wh_rect):
        points += 1
        bh_x, bh_y, wh_x, wh_y = get_hole_coords(r)

    #Extra difficulty factor: decrement points a little bit every 10 frames.
    if not points <= 0 and frames%10==0:
        points = np.round(0.99*points, 2)

    # --- draws ---
    #Draw all the things!
    bh_rect = pygame.draw.circle(win, (0, 0, 0), (bh_x, bh_y), r)
    wh_rect = pygame.draw.circle(win, (255, 255, 255), (wh_x, wh_y), r)

    #Draw player.
    pygame.draw.rect(win, (255, 0, 0), player)

    text = font.render('Points: {}'.format(points), True, green, blue)
    textRect = text.get_rect()

    win.blit(text, textRect)
    pygame.display.update()

    #Allows you to trace the player's path as long as you hold the F key.
    if not keys[pygame.K_f]:
        win.fill([0, 0, 0])
        win.blit(background_image, [0,0])

    frames += 1
    print(vel)

# --- the end ---

pygame.quit()