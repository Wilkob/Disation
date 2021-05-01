import neat
import os
import Simluation105C as Sim
import pickle
import time

gen = 0
bestof = []
avgof = []

def eval_genomes(genomes, config):
    global gen,bestof , avgof,file
    gen += 1
    nets = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)

    for x, net in enumerate(nets):
        print("Ai: ", x , "Gen: ", gen)
        ge[x].fitness = Sim.Run(net,x,gen)

def Pickling(net):
    filename = "netxx"
    outfile = open(filename, 'wb')
    pickle.dump(net, outfile)
    outfile.close()

def main():
    global bestof,avgof,file
    start = time.time()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    winner = p.run(eval_genomes, 100)
    Pickling(winner)
    end = time.time()
    print('\nBest genome:\n{!s}'.format(winner))
    print('\nTime Taken: ', (end - start))

main()