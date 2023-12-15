from graphics import *
from math import floor
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

        self.__board_object = self.__draw_board(self.__width, self.__height, self.__square_size, chance_square_is_mine)

        self.__win.getKey()
        self.__win.close()

    def __draw_board(self, width: int, height: int, square_size: int, chance_square_is_mine: float) -> list[list[Rectangle]]:
        board = []
        for y in range(0, width, square_size):
            row = []
            for x in range(0, height, square_size):
                current_square = Square(self.__win, x, y, square_size, chance_square_is_mine, SQUARE_FILL_COLOR, SQUARE_BORDER_COLOR)
                row.append(current_square)
            board.append(row)
        return board
    
    def __determine_clicked_square_index(self, click: Point) -> (int, int):
        #Todo: could refactor function because multiplying by square size and then dividing
        square_top_left_x = self.__round_down_to_square_size(click.getX())
        square_top_left_y = self.__round_down_to_square_size(click.getY())
        row_index = square_top_left_y // self.__square_size
        column_index = square_top_left_x // self.__square_size
        return (row_index, column_index)

    def __round_down_to_square_size(self, value: float) -> int:
        return int(floor(value / self.__square_size)) * self.__square_size

    def __click_board(self, click: Point) -> None:
        # Determine which square
        row_i, col_i = self.__determine_clicked_square_index(click)
        clicked_square = self.__board_object[row_i][col_i]
        clicked_square.set_fill_color("green")
        clicked_square.draw()
        # If square is mine - game over
        # Else - square.click_square()





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
        self.__fill_color = square_fill_color
        self.__border_color = square_border_color
        self.__square_graphical_object = self.__instantiate_square_graphical_object(self.__top_left_x, self.__top_left_y, self.__size, self.__fill_color, self.__border_color) 
        self.__is_mine = self.__determine_if_square_is_mine(chance_square_is_mine)
        self.__is_clicked = False
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
    board_object = Board(
        win_width= 300,
        win_height= 300,
        square_size= 20,
        chance_square_is_mine= 0.1,
        board_color= "light grey"
    )

if __name__ == '__main__':
    main()