from graphics import *

class Board:
    def __init__(self, win_width: int,
                       win_height: int,
                       num_rows: int,
                       num_cols: int,
                       chance_square_is_mine: float) -> None:
        
        self.__win = GraphWin("Minesweeper", win_width, win_height)

        # Instantiate squares

        self.__win.getKey('x')
        self.__win.close()



         

def main() -> None:
    # Define board parameters
    # Instantiate board
    # Gameplay loop
    pass

if __name__ == '__main__':
    main()