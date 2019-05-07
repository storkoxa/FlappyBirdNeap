from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pickle
import neat
import sys 

from Game import Game


def loadGenome(file):
	# Load configuration.
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 'neural_evolution.config')

	genome = pickle.load(open(file, 'rb'))
	print(genome)
	if genome is not None:
		display = pygame.display.set_mode((800,600))
		pygame.display.set_caption('Flappy Bird')
		pygame.init()
		game = Game(display)
		game.start([genome], config)



def train(n=50):
	# Load configuration.
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 'neural_evolution.config')

	p = neat.Population(config)
	winner = p.run(eval_genomes, n=n)

	# save the best bird
	pickle.dump(winner, open('winner.pkl', 'wb'))
	

def eval_genomes(genomes, config):
	display = pygame.display.set_mode((800,600))
	pygame.display.set_caption('Flappy Bird')
	pygame.init()

	# Play game and get results
	idx,genomes = zip(*genomes)
	game = Game(display)
	game.start(genomes, config)
	best = { "score": 0, "genome": None }
	for result in game.results:
		fitness = result['energy'] * -5 + result['points'] * 1000
		if (fitness > best['score']):
			best['score'] = fitness
			best['genome'] = result['genome']
		
		result['genome'].fitness = fitness

	pickle.dump(best['genome'], open('bests/fit' + str(fitness) + '_points.pkl', 'wb'))



if __name__ == '__main__':
	if (len(sys.argv) > 1):
		file = sys.argv[1]
		loadGenome(file)
	else:
		train()

