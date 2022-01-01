import os
import pygame
from pygame import Rect
from pygame.math import Vector2

os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameState():
    def __init__(self):
        self.worldSize = Vector2(16,10)
        self.tankPos = Vector2(5,4)
        self.towersPos = [
          Vector2(10, 3),
          Vector2(10, 5)
        ]
        # self.tower1Pos = Vector2(10, 3)
        # self.tower2Pos = Vector2(10, 5)

    def update(self,moveTankCommand):
        newTankPos = self.tankPos + moveTankCommand

        # Don't allow positions outside the world
        if newTankPos.x < 0 or newTankPos.x >= self.worldSize.x \
        or newTankPos.y < 0 or newTankPos.y >= self.worldSize.y:
            return

        # Don't allow tower positions 
        for position in self.towersPos:
            if newTankPos == position:
                return

        self.tankPos = newTankPos


        

class UserInterface():
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.cellSize = Vector2(64,64)
        self.unitsTexture = pygame.image.load("units.png")

        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveTankCommand = Vector2(0,0)

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        self.moveTankCommand = Vector2(0,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.moveTankCommand.x = 1
                elif event.key == pygame.K_LEFT:
                    self.moveTankCommand.x = -1
                elif event.key == pygame.K_DOWN:
                    self.moveTankCommand.y = 1
                elif event.key == pygame.K_UP:
                    self.moveTankCommand.y = -1

    def update(self):
        self.gameState.update(self.moveTankCommand)

    def render(self):
        self.window.fill((0,0,0))

        # # Tank base
        # spritePoint = self.gameState.tankPos.elementwise()*self.cellSize
        # texturePoint = Vector2(1,0).elementwise()*self.cellSize
        # textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x),int(self.cellSize.y))
        # self.window.blit(self.unitsTexture,spritePoint,textureRect)

        # #set tower positions
        # # tower 1
        # self.set_tower_position(self.gameState.towersPos[0].elementwise()*self.cellSize, 0, 1)
        # #tower 2
        # self.set_tower_position(self.gameState.towersPos[1].elementwise()*self.cellSize, 0 , 6)


        # pygame.display.update()    
        # Towers
        for position in self.gameState.towersPos:
            spritePoint = position.elementwise()*self.cellSize
            texturePoint = Vector2(0,1).elementwise()*self.cellSize
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x),int(self.cellSize.y))
            self.window.blit(self.unitsTexture,spritePoint,textureRect)
            texturePoint = Vector2(0,6).elementwise()*self.cellSize
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x),int(self.cellSize.y))
            self.window.blit(self.unitsTexture,spritePoint,textureRect)

        # Tank
        spritePoint = self.gameState.tankPos.elementwise()*self.cellSize
        texturePoint = Vector2(1,0).elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x),int(self.cellSize.y))
        self.window.blit(self.unitsTexture,spritePoint,textureRect)
        texturePoint = Vector2(0,6).elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x),int(self.cellSize.y))
        self.window.blit(self.unitsTexture,spritePoint,textureRect)

        pygame.display.update()    

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

    def set_tower_position(self, spritePoint, x, y):
      texturePoint = Vector2(x,y).elementwise()*self.cellSize
      textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x), int(self.cellSize.y))
      self.window.blit(self.unitsTexture, spritePoint, textureRect)
    


userInterface = UserInterface()
userInterface.run()

pygame.quit()
