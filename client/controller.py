import threading
from client.display import title_screen as view
from map import board, map_selection


class controller:

    def __init__(self):
        pass


if __name__ == "__main__":
    game = controller()

    #start graphics thread
    graphics = threading.Thread(target=view)
    graphics.start()
