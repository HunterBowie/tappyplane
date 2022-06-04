import neat, math
import game, windowgui, neural_net

def fitness_function(genomes, config):
    new_game = game.Game(game.window)
    new_game.config(display_score=False, managed=True, num_planes=50)
    for genome_id, genome in genomes:
        genome.fitness = 0
    timer = windowgui.Timer()
    timer.start()
    plane_dict = {genome: plane for _,genome in genomes for plane in new_game.planes}
    new_game.running = True
    while new_game.running and game.window.running:
        if timer.passed(.1):
            for genome,_ in plane_dict.items():
                genome.fitness += .1
            timer.start()

        dead_genomes = []
        for genome, plane in plane_dict.items():
            if not plane in new_game.planes:
                dead_genomes.append(genome)
    
        for genome in dead_genomes:
            del plane_dict[genome]
            print(len(plane_dict))

        for genome, plane in plane_dict.items():
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            # nearest_rock = None
            # nearest_dist = None
            # for rock in new_game.rocks:
            #     dist = math.dist(rock.get_rect().center, plane.get_real_pos())
            #     if nearest_dist is None:
            #         nearest_rock = rock
            #         nearest_dist = dist

            #     elif dist < nearest_dist:
            #         nearest_dist = dist
            #         nearest_rock = rock 
            
            plane_y = plane.get_real_pos()[1]
            output = network.activate([plane_y])
            if output[0] > 0:
                plane.boost()


        new_game.update()
        
        
        

    if not game.window.running:
        quit()
    if not new_game.running:
        pass
        #All birds died


if __name__ == "__main__":
    game.window.start()
    population = neural_net.init()
    winner = population.run(fitness_function)
    print("success")
    neural_net.save_genome(winner, "best")