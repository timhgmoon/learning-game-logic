import pygame
from pygame.math import Vector2

class UserInterface():
  def __init__(self):
    pygame.init()
    self.gameState = GameState()
    self.cellSize = Vector2(64,64)
    self.unitsTexture = pygame.image.load("towers_walls_blank.py")

    windowSize = self.gameState.worldSize.elementwise() * self.cellSize
    self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
    pygame.display.set_caption("tank moving practice")
    self.moveTankCommand = Vector2(0,0)

    self.clock = pygame.time.Clock()
    self.running = True
  def render(self):
    self.window.fill((0,0,0))
    spritePoint = self.gameState.tankPos.elementwise()*self.cellSize
    texturePoint = Vector2(1,0).elementwise()*self.cellSize
    textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x), int(self.cellSize.y))
    self.window.blit(self.unitsTexture, spritePoint, textureRect)

    pygame.display.update()

class GameState():
  def update(self, moveTankCommand):
    self.tankPos += moveTankCommand
    if self.tankPos.x < 0:
      self.tankPos.x = 0
    elif self.tankPos.x >= self.workSize.x:
      self.tankPos.x = self.worldSize.x - 1

    if self.tankPos.y < 0:
      self.tankPos.y = 0
    elif self.tankPos.y >= self.worldSize.y:
      self.tankPos.y = self.worldSize.y - 1
