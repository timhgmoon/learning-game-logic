import os
import math
import pygame
from pygame import Rect
from pygame.math import Vector2

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Unit():
    def __init__(self,state,position,tile):
        self.state = state
        self.position = position
        self.tile = tile
        self.orientation = 0
        self.weaponTarget = Vector2(0,0)
    def move(self,moveVector):
        raise NotImplementedError()    
    def orientWeapon(self,target):
        raise NotImplementedError()    

class Tank(Unit):
    def move(self,moveVector):
        # Update tank orientation
        if moveVector.x < 0: 
            self.orientation = 90
        elif moveVector.x > 0: 
            self.orientation = -90
        if moveVector.y < 0: 
            self.orientation = 0
        elif moveVector.y > 0: 
            self.orientation = 180
        
        # Compute new tank position
        newTankPos = self.position + moveVector

        # Don't allow positions outside the world
        if newTankPos.x < 0 or newTankPos.x >= self.state.worldWidth \
        or newTankPos.y < 0 or newTankPos.y >= self.state.worldHeight:
            return

        # Don't allow wall positions
        if not self.state.walls[int(newTankPos.y)][int(newTankPos.x)] is None:
            return

        # Don't allow other unit positions 
        for unit in self.state.units:
            if newTankPos == unit.position:
                return

        self.position = newTankPos

    def orientWeapon(self,target):
        self.weaponTarget = target

class Tower(Unit):
    def move(self,moveVector):
        pass
    def orientWeapon(self,target):
        self.weaponTarget = self.state.units[0].position
        mousePos = pygame.mouse.get_pos()
        
class GameState():
    def __init__(self):
        self.worldSize = Vector2(16,10)
        self.ground = [ 
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(6,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1)],
            [ Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,5), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,5), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1)],
            [ Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(6,2), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,4), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(7,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)]
        ]
        self.walls = [
            [ None, None, None, None, None, None, None, None, None, Vector2(1,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(1,3), Vector2(1,1), Vector2(0,3), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(3,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, None, None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(0,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,3), Vector2(1,1), Vector2(3,3), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)]
        ]
        self.units = [
            Tank(self,Vector2(1,9),Vector2(1,0)),
            Tower(self,Vector2(6,3),Vector2(0,2)),
            Tower(self,Vector2(6,5),Vector2(0,2)),
            Tower(self,Vector2(13,3),Vector2(0,1)),
            Tower(self,Vector2(13,6),Vector2(0,1))
        ]
    
    @property
    def worldWidth(self):
        return int(self.worldSize.x)
    
    @property
    def worldHeight(self):
        return int(self.worldSize.y)
        
    def update(self,moveTankCommand,targetCommand):
        for unit in self.units:
            unit.move(moveTankCommand)
        for unit in self.units:
            unit.orientWeapon(targetCommand)
        
class Layer():
    def __init__(self,ui,imageFile):
        self.ui = ui
        self.texture = pygame.image.load(imageFile)
        
    def renderTile(self,surface,position,tile,angle=None):
        # Location on screen
        spritePoint = position.elementwise()*self.ui.cellSize
        
        # Texture
        texturePoint = tile.elementwise()*self.ui.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), self.ui.cellWidth, self.ui.cellHeight)
        
        # Draw
        if angle is None:
            surface.blit(self.texture,spritePoint,textureRect)
        else:
            # Extract the tile in a surface
            textureTile = pygame.Surface((self.ui.cellWidth,self.ui.cellHeight),pygame.SRCALPHA)
            textureTile.blit(self.texture,(0,0),textureRect)
            # Rotate the surface with the tile
            rotatedTile = pygame.transform.rotate(textureTile,angle)
            # Compute the new coordinate on the screen, knowing that we rotate around the center of the tile
            spritePoint.x -= (rotatedTile.get_width() - textureTile.get_width()) // 2
            spritePoint.y -= (rotatedTile.get_height() - textureTile.get_height()) // 2
            # Render the rotatedTile
            surface.blit(rotatedTile,spritePoint)

    def render(self,surface):
        raise NotImplementedError() 
    
class ArrayLayer(Layer):
    def __init__(self,ui,imageFile,gameState,array):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.array = array
        
    def render(self,surface):
        for y in range(self.gameState.worldHeight):
            for x in range(self.gameState.worldWidth):
                tile = self.array[y][x]
                if not tile is None:
                    self.renderTile(surface,Vector2(x,y),tile)

class UnitsLayer(Layer):
    def __init__(self,ui,imageFile,gameState,units):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.units = units
        
    def render(self,surface):
        for unit in self.units:
            self.renderTile(surface,unit.position,unit.tile,unit.orientation)
            size = unit.weaponTarget - unit.position
            angle = math.atan2(-size.x,-size.y) * 180 / math.pi
            self.renderTile(surface,unit.position,Vector2(0,6),angle)

class UserInterface():
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.cellSize = Vector2(64,64)
        self.layers = [
            ArrayLayer(self,"ground.png",self.gameState,self.gameState.ground),
            ArrayLayer(self,"walls.png",self.gameState,self.gameState.walls),
            UnitsLayer(self,"units.png",self.gameState,self.gameState.units)
        ]

        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveTankCommand = Vector2(0,0)
        self.targetCommand = Vector2(0,0)
        
        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True
        
    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def processInput(self):

        # Pygame events (close & keyboard)
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
                    
        # Mouse handling
        mousePos = pygame.mouse.get_pos()                    
        self.targetCommand.x = mousePos[0] / self.cellWidth - 0.5
        self.targetCommand.y = mousePos[1] / self.cellHeight - 0.5
                    
    def update(self):
        self.gameState.update(self.moveTankCommand,self.targetCommand) 
        
    def render(self):
        self.window.fill((0,0,0))
        
        for layer in self.layers:
            layer.render(self.window)
        
        pygame.display.update()    
        
    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)
    
userInterface = UserInterface()
userInterface.run()

pygame.quit()
    
