import pygame
import time

pygame.init()

#colours
colour_black = (0, 0, 0)
player1_colour = (0, 255, 255)
player2_colour = (255, 0, 255)


#player class
class Player:
  #run on start
  def __init__(self, x, y, b, c):
    self.x = x
    self.y = y
    self.speed = 1
    self.bearing = b
    self.colour = c
    self.start_boost = time.time()
    self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)

  #Class functions
  def draw(self):  #bc its diff to repeatedly draw in the a loop
    self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)
    pygame.draw.rect(screen, self.colour, self.rect, 0)

  def move(self):
    self.x += self.bearing[0]
    self.y += self.bearing[1]


#Function for starting a new game, remaking player objects
def new_game():
  new_pl1 = Player(50, height / 2, [2, 0], player1_colour)
  new_pl2 = Player(width - 50, height / 2, [-2, 0], player2_colour)
  return new_pl1, new_pl2


#screen
width, height = 600, 660
offset = height - width
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tron")

#Font
font = pygame.font.Font(None, 72)

#clock
clock = pygame.time.Clock()
check_time = time.time()

#better for more complicated data structures
objects = list()
path = list()
p1 = Player(50, (height - offset) / 2, [2, 0], player1_colour)
p2 = Player(width - 50, (height - offset) / 2, [-2, 0], player2_colour)
objects.append(p1)
objects.append(p2)
path.append((p1.rect, '1'))
path.append((p2.rect, '2'))

#score
player_score = [0, 0]

#Wall rects
wall_rects = [
    pygame.Rect([0, offset, 15, height]),
    pygame.Rect([0, offset, width, 15]),
    pygame.Rect([width - 15, offset, 15, height]),
    pygame.Rect([0, height - 15, width, 15])
]

#Boolean variables
done = False
new = False

#Main while/Update loop
while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    elif event.type == pygame.KEYDOWN:
      #Player 1
      if event.key == pygame.K_w:
        objects[0].bearing = [0, -2]
      elif event.key == pygame.K_s:
        objects[0].bearing = [0, 2]
      elif event.key == pygame.K_a:
        objects[0].bearing = [-2, 0]
      elif event.key == pygame.K_d:
        objects[0].bearing = [2, 0]
      #Player 2
      if event.key == pygame.K_UP:
        objects[1].bearing = [0, -2]
      elif event.key == pygame.K_DOWN:
        objects[1].bearing = [0, 2]
      elif event.key == pygame.K_LEFT:
        objects[1].bearing = [-2, 0]
      elif event.key == pygame.K_RIGHT:
        objects[1].bearing = [2, 0]

  screen.fill(colour_black)  #fill screem for rendering

  for rect in wall_rects:  #draw rectangles
    pygame.draw.rect(screen, (42, 42, 42), rect, 0)

  for obj in objects:
    if (obj.rect, '1') in path or (obj.rect,'2') in path \
    or obj.rect.collidelist(wall_rects) > -1:
      if (time.time() - check_time) >= 0.1:
        check_time = time.time()
#IT WAS BUGGY BC THIS WAS NOT IN THE IF STATEMENT(LIKE NOT INDENTED)
        if obj.colour == player1_colour:
          player_score[1] += 1
        else:
          player_score[0] += 1
  
        new = True
        new_p1 , new_p2 = new_game()
        objects = [new_p1, new_p2]
        path = [(p1.rect , '1') , (p2.rect , '2')]
        break
    else:
      if obj.colour == player1_colour:  
         path.append((obj.rect , '1')) 
      else:
        path.append((obj.rect , '2'))
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

  pygame.display.flip()  #updates screen
  clock.tick(60)  #60 fps

pygame.quit()
