import neat, math
import game, windowgui, neural_net

config = neural_net.load_config()
genome = neural_net.load_genome("best")
network = neat.nn.FeedForwardNetwork.create(genome, config)

def run():
    new_game = game.Game(game.window)
    new_game.config(plane_color="red", display_score=False, managed=True, terrain_simple=True)
    plane = new_game.planes[0]
    new_game.running = True
    while new_game.running and game.window.running:
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

if __name__ == "__main__":
    game.window.start()
    while game.window.running:
        run()
