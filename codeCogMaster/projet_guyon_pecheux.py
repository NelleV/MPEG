# -*- coding: cp1252 -*-
###############################################################################
# Nicolas {Guyon, Pécheux} - AE - Projet Inattentional Blindness - 19 May 2011
###############################################################################

# Right mouse button, True or 1 is when vertical is longer
# So left button is 0, right button is 1

import sys, pygame, random, os
from pygame.locals import *

# Parameters

back_color = [255, 255, 255]
stimuli_color = [0, 0, 0]

fixation_time_lower = 1300
fixation_time_upper = 2000
stimulus_time = 150
mask_time = 50
thanks_time = 1000

central_cross_color = [255, 0, 0]
central_cross_length = 5

distractor_color = stimuli_color
distractor_size = 4

cross_color = stimuli_color
cross_length_short = 50
cross_length_long = 60
cross_width = 4

cross_distance = 80

# Exceptions

class Exit(Exception):
    def __init__(self):
        return

# Subject's Data

# Name begin with an number for Guyon and end with a number for Pécheux
name = raw_input('Nom ? : ')
# Age must be an integer
age = raw_input('Age ? : ')
# Gender is "m" or "f"
gender = raw_input('Sexe ? : ')
# Category is 1 for Denis' classroom, 2 for Chaillou's classroom and 3 for adults
category = raw_input('Category ? : ')

# Initialization

pygame.init()

screen = pygame.display.set_mode([0, 0], FULLSCREEN)
W, H = screen.get_size()
pygame.mouse.set_visible(False)

# Load mask
mask_image = pygame.image.load('mask.bmp')
x_mask, y_mask = mask_image.get_size()

# Choose once for all cross position at random in one of the four squares
x_cross_place, y_cross_place = (2*random.randint(0, 1) - 1), (2*random.randint(0, 1) - 1)
x_cross_pos, y_cross_pos = W/2 + x_cross_place*cross_distance, H/2 + y_cross_place*cross_distance

# Display message
police = pygame.font.SysFont("arial", 60)
ready_message = police.render('Prêt ?', 1, stimuli_color)
ready_rect = ready_message.get_rect()
ready_rect.center = (W/2, H/2)

police = pygame.font.SysFont("arial", 60)
thanks_message = police.render('Merci !', 1, stimuli_color)
thanks_rect = thanks_message.get_rect()
thanks_rect.center = (W/2, H/2)

# Result file
file = open(os.path.join('results', name), 'at')
file.write(name + ' ' + age + ' ' + gender + ' ' + category + ' (' + str(x_cross_place) + ', ' + str(y_cross_place) + ')\n\n')

# Displaying functions

def central_cross():
    pygame.draw.line(screen, central_cross_color, [W/2 - central_cross_length, H/2], [W/2 + central_cross_length, H/2])
    pygame.draw.line(screen, central_cross_color, [W/2, H/2 - central_cross_length], [W/2, H/2 + central_cross_length])

def distractor(pos):
    pygame.draw.circle(screen, distractor_color, pos, distractor_size)
    
def cross(x_pos, y_pos, vertical_longer):
    if vertical_longer:
        cross_vertical, cross_horizontal = cross_length_long, cross_length_short
    else:
        cross_vertical, cross_horizontal = cross_length_short, cross_length_long
        
    pygame.draw.line(screen, cross_color, [x_pos - cross_horizontal, y_pos], [x_pos + cross_horizontal, y_pos], cross_width)
    pygame.draw.line(screen, cross_color, [x_pos, y_pos - cross_vertical], [x_pos, y_pos + cross_vertical], cross_width)

def mask():
    screen.blit(mask_image, (W/2 - x_mask/2, H/2 - y_mask/2))
    pygame.display.flip()

# Main functions

def get_response():
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise Exit
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    raise Exit
            elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return 0     # left, horizontal longer
                    elif event.button == 3:
                        return 1    # rigth, vertical longer
def ready():
    screen.fill(back_color)
    screen.blit(ready_message, ready_rect)
    pygame.display.flip()

def thanks():
    screen.fill(back_color)
    screen.blit(thanks_message, thanks_rect)
    pygame.display.flip()

def do_trial(is_distractor, vertical_longer, fixation_time):
    screen.fill(back_color)
    # Blit central cross
    central_cross()
    pygame.display.flip()
    pygame.time.wait(fixation_time)
    # Blit cross (and distractor)
    if is_distractor: distractor([W/2, H/2])
    cross(x_cross_pos, y_cross_pos, vertical_longer)
    pygame.display.flip()
    pygame.time.wait(stimulus_time)
    # Blit mask
    mask()
    pygame.display.flip()
    pygame.time.wait(mask_time)

try:

    #Explanation
    vertical_longer = random.random() < 0.5
    screen.fill(back_color)
    central_cross()
    pygame.display.flip()
    get_response()
    cross(x_cross_pos, y_cross_pos, vertical_longer)
    pygame.display.flip()
    get_response()
    mask()
    pygame.display.flip()
    get_response()
    
    #Training
    ready()
    get_response()
    
    for trial in range(3):
        vertical_longer = random.random() < 0.5
        fixation_time = random.randint(fixation_time_lower, fixation_time_upper)
        do_trial(False, vertical_longer, fixation_time)
        resp = get_response()
        file.write(str(fixation_time) + ' ' + str(int(vertical_longer)) + ' ' + str(resp) + ' ' + str(int(int(vertical_longer) == resp)) + '\n')

    file.write('\n\n')
    thanks()
    pygame.time.wait(thanks_time)

    #Test sequence
    for test in range(3):
        
        ready()
        get_response()

        for trial in range (2):
            vertical_longer = random.random() < 0.5
            fixation_time = random.randint(fixation_time_lower, fixation_time_upper)
            do_trial(False, vertical_longer, fixation_time)
            resp = get_response()
            file.write(str(fixation_time) + ' ' + str(int(vertical_longer)) + ' ' + str(resp) + ' ' + str(int(int(vertical_longer) == resp)) + '\n')

        vertical_longer = random.random() < 0.5
        fixation_time = random.randint(fixation_time_lower, fixation_time_upper)                                  
        do_trial(True, vertical_longer, fixation_time)
        resp = get_response()
        file.write(str(fixation_time) + ' ' + str(int(vertical_longer)) + ' ' + str(resp) + ' ' + str(int(int(vertical_longer) == resp)) + '\n\n')               

        thanks()
        pygame.time.wait(thanks_time)

    pygame.quit()    

    resp1 = raw_input('Detecté essai 1 ? : ')
    resp2 = raw_input('Detecté essai 2 ? : ')
    resp3 = raw_input('Detecté essai 3 ? : ')
    rem = raw_input('Remarques ? : ')
    file.write(resp1 + ' ' + resp2 + ' ' + resp3 + '\n')
    file.write(rem + '\n')

    file.close()
        
except Exit:
    pass
    
finally:    
    file.close()
    pygame.quit()
    #sys.exit()
