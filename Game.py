import pygame
import neat

from Bird import Bird
from Pipe import Pipe
from Config import Config

class Game:
	birds = []
	pipes = []
	lastPipeCreated = Config['pipe']['delay'];
	points = 0
	myfont = None
	results = []

	def __init__(self, display):
		self.display = display
		self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
		print("game was initialized")



	def draw(self):
		self.display.fill((0,0,0))
		for bird in self.birds:
			bird.draw()
		for pipe in self.pipes:
			pipe.draw()
		textsurface = self.myfont.render('Points: ' + str(self.points), False, (255, 0, 0))
		self.display.blit(textsurface,(0,0))




	def start(self, genomes, config):
		self.points = 0
		self.lastPipeCreated = Config['pipe']['delay']
		self.pipes = []
		self.results = []
		for genome in genomes:
			self.birds.append(Bird(self.display, genome, config))
		self.loop()



	def update(self, tick): 
		self.lastPipeCreated += 1
		if (self.lastPipeCreated >= Config['pipe']['delay']):
			self.pipes.append(Pipe(self.display))
			self.lastPipeCreated = 0
		for pipe in self.pipes:
			removePipe = pipe.update()
			if removePipe:
				self.points += 1
				self.pipes.remove(pipe)

		for bird in self.birds:
			bird.update()
			bird.think(self.pipes)			
			if bird.isDead(self.pipes):
				self.results.append({'genome': bird.genome, 'energy': bird.energy, 'points': self.points})
				self.birds.remove(bird)
		





	def loop(self):
		clock = pygame.time.Clock()
		while True:
			dt = clock.tick(Config['game']['fps']);
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

			self.update(dt)
			if (len(self.birds) == 0):
					return;

			self.draw()

			pygame.display.update()
			
