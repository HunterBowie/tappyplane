import pickle, os, neat
import constants

def load_config():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, constants.CONFIG_FILE)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    return config

def load_population():
    config = load_config()

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    return population

def save_genome(genome, file_name):
    pickle.dump(genome, open(file_name+".pickle", "wb"))

def load_genome(file_name):
    return pickle.load(open(file_name+".pickle", "rb"))