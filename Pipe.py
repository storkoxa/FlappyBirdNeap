import pygame
import random 

from Config import Config

class Pipe:
	gapY = 0

	topPipe = None
	bottomPipe = None

	def __init__(self, display):
		x, y = display.get_size()		

		self.display = display
		gap = Config['pipe']['gap'];
		width = Config['pipe']['width']
		self.gapY = random.randint(0, y - gap)

		self.topPipe = pygame.Rect(x, 0, width, self.gapY)
		self.bottomPipe = pygame.Rect(x, self.gapY + gap, width, y - (self.gapY + gap))

	def getX(self): 
		return self.topPipe.x

	def draw(self):
		pygame.draw.rect(self.display, (200, 200, 200), self.topPipe)
		pygame.draw.rect(self.display, (200, 200, 200), self.bottomPipe)

	def update(self): 
		self.topPipe = self.topPipe.move(Config['pipe']['velocity'], 0)
		self.bottomPipe = self.bottomPipe.move(Config['pipe']['velocity'], 0)
		return self.isOffScreen()

	def isOffScreen(self):
		return self.topPipe.x < -Config['pipe']['width']