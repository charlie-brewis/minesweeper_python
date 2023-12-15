from graphics import *
import random

class Board:
    def __init__(self, win_width: int,
                       win_height: int,
                       num_rows: int,
                       num_cols: int,
                       chance_square_is_mine: float,
                       board_color: str) -> None:
        
        self.__win = GraphWin("Minesweeper", win_width, win_height)

        # Instantiate squares

        self.__win.getKey('x')
        self.__win.close()


class Square:
    def __init__(self, win: GraphWin,
                       top_left_x: int, 
                       top_left_y: int, 
                       square_size: int, 
                       chance_square_is_mine: float, 
                       square_color: str) -> None:
        
        self.__top_left_x = top_left_x
        self.__top_left_y = top_left_y
        self.__size = square_size
        self.__is_mine = self.__determine_if_square_is_mine(chance_square_is_mine)
        self.__color = square_color
        self.__square_graphical_object = self.__instantiate_square_graphical_object(self.__top_left_x, self.__top_left_y, self.__size, self.__color) 
        self.draw()

    def __determine_if_square_is_mine(self, chance_square_is_mine: float) -> bool:
        return random.random() < chance_square_is_mine
    
    def __instantiate_square_graphical_object(self, top_left_x: int, top_left_y: int, square_size: int, square_color: str) -> Rectangle:
        top_left_point = Point(top_left_x, top_left_y)
        bottom_right_point = Point(top_left_x + square_size, top_left_y + square_size)
        square_graphical_object = Rectangle(top_left_point, bottom_right_point)
        square_graphical_object.setFill(square_color)
        return square_graphical_object
    
    def draw(self) -> None:
        self.__square_graphical_object.draw(self.__win)

    def get_is_mine(self) -> bool:
        return self.__is_mine
    
    def get_top_left_point(self) -> Point:
        return self.__square_graphical_object.getP1()
    
    def set_color(self, new_color: str) -> None:
        self.__square_graphical_object.setFill(new_color)
        self.draw()
        

def main() -> None:
    # Define board parameters
    # Instantiate board
    # Gameplay loop
    pass

if __name__ == '__main__':
    main()