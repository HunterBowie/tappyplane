import neat, math, random
import game, windowgui, neural_net

def move_by_degrees(angle, speed):
    radians = math.radians(-angle) 
    x, y = speed * math.cos(radians), speed * math.sin(radians)
    return round(x), round(y)

def fitness_function(genomes, config):
    print(len(genomes))
    if len(genomes) < 50:
        genomes.append(random.choice(genomes))
    new_game = game.Game(game.window)
    new_game.config(display_score=False, managed=True, num_planes=50, plane_color="random")
    for genome_id, genome in genomes:
        genome.fitness = 0


    active_genomes = {}
    
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
                top_pos = plane.x, 0
                bottom_pos = plane.x, game.window.screen.get_height()
                top_height = 0
                bottom_height = 0
                top_dist = game.window.screen.get_width()*5
                bottom_dist = game.window.screen.get_width()*5
                for rock in new_game.rocks:
                    if rock.get_rect().center[0] > plane.x:
                        if rock.direction == "up":
                            dist = round(math.dist(bottom_pos, rock.get_rect().bottomleft))

                            if dist < bottom_dist:
                                bottom_dist = dist
                                bottom_height = 239 if rock.size == "large" else 120
                        else:
                            dist = round(math.dist(top_pos, rock.get_rect().topleft))
                                
                            if dist < top_dist:
                                top_dist = dist
                                top_height = 239 if rock.size == "large" else 120
                

                plane_y = plane.get_real_pos()[1]
                output = network.activate([plane_y, top_height, top_dist, bottom_height, bottom_dist])
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


# plane_rect = plane.get_static_rect()
# plane_rect.x, plane_rect.y = plane.get_real_pos()
# plane_pos = plane_rect.midright
# for rock in new_game.rocks:
#     rock_pos = rock.get_rect().midleft
#     dist = math.dist(rock_pos, plane_pos)
#     if nearest_dist is None:
#         nearest_rock = rock
#         nearest_dist = dist

#     elif dist < nearest_dist:
#         nearest_dist = dist
#         nearest_rock = rock

            