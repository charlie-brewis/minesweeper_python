from graphics import *
import random

SQUARE_FILL_COLOR = "grey"
SQUARE_BORDER_COLOR = "black"

class Board:
    def __init__(self, win_width: int,
                       win_height: int,
                       square_size: int,
                       chance_square_is_mine: float,
                       board_color: str) -> None:
        
        self.__height = win_height
        self.__width = win_width
        self.__square_size = square_size
        
        self.__win = GraphWin("Minesweeper", self.__width, self.__height)

        # Instantiate squares


        self.__win.getKey('x')
        self.__win.close()

    def __create_board(self, width: int, height: int, square_size: int, chance_square_is_mine: float) -> list[list[Rectangle]]:
        board = []
        for y in range(0, width, square_size):
            row = []
            for x in range(0, height, square_size):
                current_square = Square(self.__win, x, y, square_size, chance_square_is_mine, SQUARE_FILL_COLOR, SQUARE_BORDER_COLOR)
                row.append()




class Square:
    def __init__(self, win: GraphWin,
                       top_left_x: int, 
                       top_left_y: int, 
                       square_size: int, 
                       chance_square_is_mine: float, 
                       square_fill_color: str,
                       square_border_color: str) -> None:
        
        self.__win = win
        self.__top_left_x = top_left_x
        self.__top_left_y = top_left_y
        self.__size = square_size
        self.__is_mine = self.__determine_if_square_is_mine(chance_square_is_mine)
        self.__fill_color = square_fill_color
        self.__border_color = square_border_color
        self.__square_graphical_object = self.__instantiate_square_graphical_object(self.__top_left_x, self.__top_left_y, self.__size, self.__fill_color, self.__border_color) 
        self.draw()

    def __determine_if_square_is_mine(self, chance_square_is_mine: float) -> bool:
        return random.random() < chance_square_is_mine
    
    def __instantiate_square_graphical_object(self, top_left_x: int, top_left_y: int, square_size: int, square_fill_color: str, square_border_color: str) -> Rectangle:
        top_left_point = Point(top_left_x, top_left_y)
        bottom_right_point = Point(top_left_x + square_size, top_left_y + square_size)
        square_graphical_object = Rectangle(top_left_point, bottom_right_point)
        square_graphical_object.setFill(square_fill_color)
        square_graphical_object.setOutline(square_border_color)
        return square_graphical_object
    
    def draw(self) -> None:
        self.__square_graphical_object.draw(self.__win)

    def get_is_mine(self) -> bool:
        return self.__is_mine
    
    def get_top_left_point(self) -> Point:
        return self.__square_graphical_object.getP1()
    
    # Note: set methods do not redraw the square, this must be done seperately
    def set_fill_color(self, new_color: str) -> None:
        self.__square_graphical_object.setFill(new_color)

    def set_border_color(self, new_color: str) -> None:
        self.__square_graphical_object.setOutline(new_color)


def main() -> None:
    # Define board parameters
    # Instantiate board
    # Gameplay loop
    pass

if __name__ == '__main__':
    main()