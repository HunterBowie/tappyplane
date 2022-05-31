import game, windowgui, neural_net



def fitness_function(genomes, config):
    new_game = game.Game()
    new_game.config(display_score=False, managed=True, num_planes=50)

    game.running = True
    while game.running and game.window.running:
        game.update()
        

    if not window.running:
        quit()
    if not game.running:
        pass
        #All birds died


if __name__ == "__main__":
    population = neural_net.init()
    winner = population.run(fitness_function, 50)
    print("success")
    neural_net.save_genome(winner, "best")