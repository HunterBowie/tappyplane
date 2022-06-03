import neat, math
import game, windowgui, neural_net

def fitness_function(genomes, config):
    new_game = game.Game(game.window)
    new_game.config(display_score=False, managed=True, num_planes=25)
    for genome_id, 

    new_game.running = True
    while new_game.running and game.window.running:
        for counter, genome_parts in enumerate(genomes):
            genome = genome_parts[1]
            plane = new_game.planes[counter]
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            nearest_rock = None
            nearest_dist = None
            for rock in new_game.rocks:
                dist = math.dist(rock.get_rect().center, plane.get_real_pos())
                if nearest_dist is None:
                    nearest_rock = rock
                    nearest_dist = dist

                elif dist < nearest_dist:
                    nearest_dist = dist
                    nearest_rock = rock 
            
            plane_y = plane.get_real_pos()[1]
            x_dist = -1
            x = plane.get_real_pos()[0]
            for i in range(int(game.constants.WIDTH-x)):
                for rock in new_game.rocks:
                    if rock.colllidepoint((x+i, plane_y)):
                        x_dist = abs(x-rock.x)
                        break
                if dist != -1:
                    break
            
            output = network.activate([plane_y, x_dist, 0])
            if output[0] > 0:
                plane.boost()
            plane.fitness += 0.1
        new_game.update()
        

    if not game.window.running:
        print("died")
        quit()
    if not new_game.running:
        pass
        #All birds died


if __name__ == "__main__":
    game.window.start()
    population = neural_net.init()
    winner = population.run(fitness_function, 25)
    print("success")
    neural_net.save_genome(winner, "best")