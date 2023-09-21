import threading
from game_of_life import GameOfLife
from game_of_life_app import App
from real_time_graph_script import RealTimeGraph


def start_game_of_life_app(game_of_life):
    app = App(game_of_life)
    app.run()


def start_real_time_graph(game_of_life):
    graph = RealTimeGraph(game_of_life)
    graph.run()


if __name__ == "__main__":
    shared_game_of_life = GameOfLife(1000, 1000)

    game_thread = threading.Thread(
        target=start_game_of_life_app, args=(shared_game_of_life,))
    graph_thread = threading.Thread(
        target=start_real_time_graph, args=(shared_game_of_life,))

    game_thread.start()

    graph_thread.start()

    game_thread.join()
    graph_thread.join()
