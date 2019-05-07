import pygame
import math
import random 
import neat

from Config import Config

class Bird:
	posX = 30
	posY = 0
	velocity = 0
	energy = 0
	genome = None
	neuralNetwork = None

	def __init__(self, display, genome, config):
		self.posY = random.randint(0,200)
		self.display = display
		self.genome = genome
		self.neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, config)


	def draw(self):
		pygame.draw.circle(self.display, (0, 255, 0), (self.posX, int(self.posY)), Config['bird']['size'])
		
	def update(self):
		self.velocity += Config['physics']['gravity']
		self.posY += self.velocity
		if (self.posY <  Config['bird']['size']):
			self.velocity = Config['physics']['gravity']
		self.posY = max(self.posY, 0)


	def think(self, pipes):
		closestPipe = None
		for pipe in pipes:
			if (pipe.getX() > self.posX):
				if (closestPipe is None or closestPipe.getX() > pipe.getX()):
					closestPipe = pipe
		if (closestPipe is not None):			
			input = [closestPipe.getX(), closestPipe.gapY, Config['pipe']['gap'], self.posY, self.velocity]
			output = self.neuralNetwork.activate(input)
			if (output[0] > output[1]):
					self.goUp();
	


	def goUp(self):
		self.energy += 1
		if self.velocity >= -5:
			if self.velocity > 0:
				self.velocity = 0
			self.velocity += Config['bird']['lift']



	def isDead(self, pipes): 
		x, y = self.display.get_size()		
		if ((self.posY + Config['bird']['size']) > y):
			return True
		for pipe in pipes:
			if (self.collision(pipe.topPipe) or self.collision(pipe.bottomPipe)):
				return True;


	def collision(self, rect):  
		radius = Config['bird']['size'];
		angles = [0, 45, 90, 135, 180, 225, 270]
		for angle in angles:
			x = int(self.posX + radius * math.sin(angle))
			y = int(self.posY + radius * math.cos(angle))
			if (rect.collidepoint(x, y)):
				return True
		return False