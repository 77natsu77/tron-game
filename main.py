import pygame
import time

pygame.init()

#Colours
colour_black = (0, 0, 0)
player1_colour = (0, 255, 255)
player2_colour = (255, 0, 255)
walls_colour = (42, 42, 42)
text_colour = (230, 160, 102)


#Player Class
class Player:

  def __init__(self, x, y, b, c):  #Run on Start
    self.x = x
    self.y = y
    self.speed = 1
    self.bearing = b
    self.colour = c
    self.start_boost = time.time()
    self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)

  #Class Functions
  def draw(self):
    self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)
    pygame.draw.rect(screen, self.colour, self.rect, 0)

  def move(self):
    self.x += self.bearing[0]
    self.y += self.bearing[1]


#Function for starting a new game, remaking player objects
def new_game():
  new_p1 = Player(50, height / 2, (2, 0), player1_colour)
  new_p2 = Player(width - 50, height / 2, (-2, 0), player2_colour)
  return new_p1, new_p2


#Screen
width, height = 600, 660
offset = height - width
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tron")

#Font
font = pygame.font.Font(None, 72)
#font = pygame.font.SysFont("comic sans" , 50) cant use this on replit

#Clock
clock = pygame.time.Clock()
check_time = time.time()

#Make objects and add them to list
objects = list()
path = list()
p1, p2 = new_game()
objects.append(p1)
objects.append(p2)
path.append((p1.rect, '1'))
path.append((p2.rect, '2'))

#Score
player_score = [0, 0]

#Wall Rects
wall_rects = [
    pygame.Rect([0, offset, 15, height]),
    pygame.Rect([0, offset, width, 15]),
    pygame.Rect([width - 15, offset, 15, height]),
    pygame.Rect([0, height - 15, width, 15])
]

#Boolean Variables
done = False
new = False

#Main While/Update Loop
while not done:
  for event in pygame.event.get():  #For loop for quit
    if event.type == pygame.QUIT:
      done = True
    elif event.type == pygame.KEYDOWN:
      #Player 1
      if event.key == pygame.K_w:
        objects[0].bearing = (0, -2)
      elif event.key == pygame.K_s:
        objects[0].bearing = (0, 2)
      elif event.key == pygame.K_a:
        objects[0].bearing = (-2, 0)
      elif event.key == pygame.K_d:
        objects[0].bearing = (2, 0)
      #Player 2
      if event.key == pygame.K_UP:
        objects[1].bearing = (0, -2)
      elif event.key == pygame.K_DOWN:
        objects[1].bearing = (0, 2)
      elif event.key == pygame.K_LEFT:
        objects[1].bearing = (-2, 0)
      elif event.key == pygame.K_RIGHT:
        objects[1].bearing = (2, 0)

  screen.fill(colour_black)  #Fill screen for rendering

  for rect in wall_rects:  #Draw rectangles
    pygame.draw.rect(screen, walls_colour, rect, 0)

  for obj in objects:
    if (obj.rect, '1') in path or (obj.rect, '2') in path \
       or obj.rect.collidelist(wall_rects) > -1:
      if (time.time() - check_time) >= 0.1:
        check_time = time.time()

        if obj.colour == player1_colour:
          player_score[1] += 1
        else:
          player_score[0] += 1

        new = True
        new_p1, new_p2 = new_game()
        objects = [new_p1, new_p2]
        path = [(p1.rect, '1'), (p2.rect, '2')]
        break
    else:
      path.append(
          (obj.rect, '1')) if obj.colour == player1_colour else path.append(
              (obj.rect, '2'))

    obj.draw()
    obj.move()

  for rect in path:
    if new is True:
      path = []
      new = False
      break
    if rect[1] == '1':
      pygame.draw.rect(screen, player1_colour, rect[0], 0)
    else:
      pygame.draw.rect(screen, player2_colour, rect[0], 0)

  score_text = font.render(
      '{0} : {1}'.format(player_score[0], player_score[1]), 1, text_colour)
  score_text_pos = score_text.get_rect()
  score_text_pos.centerx = int(width / 2)
  score_text_pos.centery = int(offset / 2)
  screen.blit(score_text, score_text_pos)

  pygame.display.flip()  #Flip and tick
  clock.tick(60)

pygame.quit()
