import pygame
from pygame.locals import *
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
pygame.display.set_caption("My game(tutorial)")
# iconImage = pygame.image.load("icon.png")
# pygame.display.set_icon(iconImage)

class App:
  def __init__(self):
    self._running = True
    self._display_surf = None
    self.size = self.weight, self.height = 640, 480
    self.x = 120
    self.y = 120

  def on_init(self):
    pygame.init()
    self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
    self._running = True
  
  # def on_event(self, event):
  #   if event.type == pygame.QUIT:
  #     self._running = False
  #   elif event.type == pygame.KEYDOWN:
  #     if event.key == pygame.K_ESCAPE:
  #         self._running = False
  #         break
  #     elif event.key == pygame.K_RIGHT:
  #         self.x += 8
  #     elif event.key == pygame.K_LEFT:
  #         self.x -= 8
  #     elif event.key == pygame.K_DOWN:
  #         self.y += 8
  #     elif event.key == pygame.K_UP:
  #         self.y -= 8

  def on_loop(self):
    self._display_surf.fill((0,0,0))
    pygame.draw.rect(self._display_surf,(0,0,255),(self.x, self.y,400,240))
    pygame.display.update()
  
  def on_render(self):
    pass

  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    if self.on_init() == False:
      self._running = False

    while(self._running):
      for event in pygame.event.get():
        # self.on_event(event)
        if event.type == pygame.QUIT:
          self._running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
              self._running = False
              break
          elif event.key == pygame.K_RIGHT:
              self.x += 8
          elif event.key == pygame.K_LEFT:
              self.x -= 8
          elif event.key == pygame.K_DOWN:
              self.y += 8
          elif event.key == pygame.K_UP:
              self.y -= 8
      clock.tick(60)
      self.on_loop()
      self.on_render()

    self.on_cleanup()

if __name__ == "__main__":
  theApp = App()
  theApp.on_execute()