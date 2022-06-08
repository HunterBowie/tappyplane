import neat, math, random
import game, windowgui, neural_net

def fitness_function(genomes, config):
    new_game = game.Game(game.window)
    new_game.config(display_score=False, managed=True, num_planes=50)
    for genome_id, genome in genomes:
        genome.fitness = 0


    active_genomes = {}
    print(len(new_game.planes), len(genomes))
    for i in range(50):
        active_genomes[genomes[i][1]] = new_game.planes[i]
    new_game.running = True
    while new_game.running and game.window.running:
        

        dead_genomes = []
        for genome, plane in active_genomes.items():
            if not plane in new_game.planes:
                dead_genomes.append(genome)
    
        for genome in dead_genomes:
            del active_genomes[genome]
            
        for genome, plane in active_genomes.items():
            genome.fitness += 1/game.window.max_fps

        for genome, plane in active_genomes.items():
                network = neat.nn.FeedForwardNetwork.create(genome, config)
                nearest_rock = None
                nearest_dist = None
                plane_rect = plane.get_static_rect()
                plane_rect.x, plane_rect.y = plane.get_real_pos()
                plane_pos = plane_rect.midright
                for rock in new_game.rocks:
                    rock_pos = rock.get_rect().midleft
                    dist = math.dist(rock_pos, plane_pos)
                    if nearest_dist is None:
                        nearest_rock = rock
                        nearest_dist = dist

                    elif dist < nearest_dist:
                        nearest_dist = dist
                        nearest_rock = rock
                plane_y = plane.get_real_pos()[1]
                output = network.activate([plane_y, nearest_dist, plane.angle])
                if output[0] > 0.5:
                    plane.boost()

        new_game.update()
        
        
        

    if not game.window.running:
        quit()
    if not new_game.running:
        print()


if __name__ == "__main__":
    game.window.start()
    population = neural_net.init()
    winner = population.run(fitness_function)
    print("success")
    neural_net.save_genome(winner, "best")



            