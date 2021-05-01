import neat
import os
import Simluation103 as Sim3
import Simluation104 as Sim4
import Simluation105 as Sim5
import Simluation105C as Sim5C
import pickle


def unpickle(file):
    filename = file
    infile = open(filename, 'rb')
    p = pickle.load(infile)
    infile.close()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    print ("AI unloaded")
    AI = neat.nn.FeedForwardNetwork.create(p, config)
    return AI

def unpickle3():
    filename = "net103"
    infile = open(filename, 'rb')
    p = pickle.load(infile)
    infile.close()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward-old.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    print ("AI unloaded")
    AI = neat.nn.FeedForwardNetwork.create(p, config)
    return AI

def main():

    AI = unpickle("net105C")
    x = 0
    for x in range(50):
        Sim5C.Run(AI)
main()