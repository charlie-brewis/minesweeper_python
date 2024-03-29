from graphics import *
from math import floor
from random import random

SQUARE_FILL_COLOR = "grey"
SQUARE_BORDER_COLOR = "black"

class Game:
    def __init__(self) -> None:
        print("Game object intialised")
    
    def instantiate_board(self, board_size: int, num_squares: int, mine_chance: float) -> None:
        self.__win_size = board_size
        # Note num_squares is the number of squares along the axis, i.e., the board is num_squares x num_squaresa
        self.__num_squares = num_squares
        # Ensures that the squares tile neatly
        self.__win_size -= self.__win_size % self.__num_squares
        self.__win = GraphWin("Minesweeper", self.__win_size, self.__win_size)
        self.__board_object = Board(
            win= self.__win,
            square_size= self.__win_size // self.__num_squares,
            chance_square_is_mine= mine_chance,
        )
        print("Board object initialised")
            
    def main_loop(self) -> int:
        running = True
        score = 0
        while running:
            click = self.__win.getMouse()
            running = not self.__board_object.click_board(click)
            score += 1
        print(score)
        return score - 1

    def game_over_screen(self, score: int) -> bool:
        center_x, center_y = self.__win_size // 2, self.__win_size // 2
        game_over_message = Text(Point(center_x, center_y - (self.__win_size // 4)), f"GAME OVER\n SCORE: {score}")
        game_over_message.setSize(20)
        game_over_message.draw(self.__win)

        instructions_message = Text(Point(center_x, center_y + (self.__win_size // 5)), "Click the box to restart or anywhere else to close")
        instructions_message.setSize(10)
        instructions_message.draw(self.__win)

        restart_box_tl = Point(center_x - (self.__win_size // 3), center_y - (self.__win_size // 10))
        restart_box_br = Point(center_x + (self.__win_size // 3), center_y + (self.__win_size // 10))
        restart_box = Rectangle(restart_box_tl, restart_box_br)
        restart_box.setFill("yellow")
        restart_box.setOutline("black")
        restart_box.draw(self.__win)

        #TODO: can maybe simplify this maths
        restart_box_center_x = restart_box_tl.getX() + (restart_box_br.getX() - restart_box_tl.getX()) // 2
        restart_box_center_y = restart_box_tl.getY() + (restart_box_br.getY() - restart_box_tl.getY()) // 2
        restart_message = Text(Point(restart_box_center_x, restart_box_center_y), "RESTART")
        restart_message.setSize(15)
        restart_message.draw(self.__win)

        click = self.__win.getMouse()
        click_x, click_y = click.getX(), click.getY()
        return all([
            click_x >= restart_box_tl.getX(),
            click_x <= restart_box_br.getX(),
            click_y >= restart_box_tl.getY(),
            click_y <= restart_box_br.getY()
        ])
    
    def close_window(self) -> None:
        self.__win.close()


class Board:
    def __init__(self, win: GraphWin,
                       square_size: int,
                       chance_square_is_mine: float) -> None:
        
        self.__win = win
        self.__height = self.__win.getHeight()
        self.__width = self.__win.getWidth()
        self.__square_size = square_size
        self.__last_row_i = self.__height // self.__square_size - 1
        self.__last_col_i = self.__width // self.__square_size - 1
        self.__board_object = self.__draw_board(self.__width, self.__height, self.__square_size, chance_square_is_mine)
        self.__determine_all_square_numbers()
        self.__selected_square = None


    def __draw_board(self, width: int, height: int, square_size: int, chance_square_is_mine: float) -> list[list[Rectangle]]:
        board = []
        for y in range(0, width, square_size):
            row = []
            for x in range(0, height, square_size):
                current_square = Square(self.__win, x, y, square_size, chance_square_is_mine, SQUARE_FILL_COLOR, SQUARE_BORDER_COLOR)
                row.append(current_square)
            board.append(row)
        return board
    
    def __determine_all_square_numbers(self):
        for row_i in range(0, self.__last_row_i + 1):
            for col_i in range(0, self.__last_col_i + 1):
                #! Surely there is someway we can define this outside the loop?
                border_square_indexes = [
                    (row_i - 1, col_i),
                    (row_i - 1, col_i + 1),
                    (row_i , col_i + 1),
                    (row_i + 1, col_i + 1),
                    (row_i + 1, col_i),
                    (row_i + 1, col_i - 1),
                    (row_i , col_i - 1),
                    (row_i - 1, col_i - 1),
                ]
                square = self.__board_object[row_i][col_i]
                if square.get_is_mine():
                    # print(square.get_number(), end=' ')
                    continue
                square_num = 0
                for adjacent_square_row_i, adjacent_square_col_i in border_square_indexes:
                    if self.__check_square_in_bounds(adjacent_square_row_i, adjacent_square_col_i):
                        adjacent_square = self.__board_object[adjacent_square_row_i][adjacent_square_col_i]
                        if adjacent_square.get_is_mine():
                            square_num += 1
                square.set_number(square_num)
            #     print(square.get_number(), end=' ')
            # print("")

    def __check_square_in_bounds(self, row_i: int, col_i: int) -> bool:
        in_bounds_conditions = [
            row_i >= 0,
            row_i <= self.__last_row_i,
            col_i >= 0,
            col_i <= self.__last_col_i
        ]
        return all(in_bounds_conditions)

    def __determine_clicked_square_index(self, click: Point) -> (int, int):
        #Todo: could refactor function because multiplying by square size and then dividing
        square_top_left_x = self.__round_down_to_square_size(click.getX())
        square_top_left_y = self.__round_down_to_square_size(click.getY())
        row_index = square_top_left_y // self.__square_size
        column_index = square_top_left_x // self.__square_size
        return (row_index, column_index)

    def __round_down_to_square_size(self, value: float) -> int:
        return int(floor(value / self.__square_size)) * self.__square_size
    

    def __open_square(self, row_i: int, col_i: int) -> bool:
        square = self.__board_object[row_i][col_i]
        square.open()
        square_num = square.get_number()
        if square_num < 0:
            return True
        if square_num == 0:
            bounding_indexes = [
                (row_i - 1, col_i),
                (row_i - 1, col_i + 1),
                (row_i , col_i + 1),
                (row_i + 1, col_i + 1),
                (row_i + 1, col_i),
                (row_i + 1, col_i - 1),
                (row_i , col_i - 1),
                (row_i - 1, col_i - 1),
            ]
            for adjacent_square_row_i, adjacent_square_col_i in bounding_indexes:
                if self.__check_square_in_bounds(adjacent_square_row_i, adjacent_square_col_i) and not self.__board_object[adjacent_square_row_i][adjacent_square_col_i].get_is_revealed():
                    self.__open_square(adjacent_square_row_i, adjacent_square_col_i)
        return False

    def click_board(self, click: Point) -> bool:
        # Determine which square
        row_i, col_i = self.__determine_clicked_square_index(click)
        square = self.__board_object[row_i][col_i]
        if not square.get_is_revealed():
            if self.__selected_square:
                self.__selected_square.deselect()
            # square.select()
            self.__selected_square = square
            square.select()
            return self.__open_square(row_i, col_i)
        return False


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
        self.__is_revealed = False
        self.__square_graphical_object.draw(self.__win)
        self.__number = -1
        self.__is_selected = False

    def __determine_if_square_is_mine(self, chance_square_is_mine: float) -> bool:
        return random() < chance_square_is_mine
    
    def __instantiate_square_graphical_object(self, top_left_x: int, top_left_y: int, square_size: int, square_fill_color: str, square_border_color: str) -> Rectangle:
        top_left_point = Point(top_left_x, top_left_y)
        bottom_right_point = Point(top_left_x + square_size, top_left_y + square_size)
        square_graphical_object = Rectangle(top_left_point, bottom_right_point)
        square_graphical_object.setFill(square_fill_color)
        square_graphical_object.setOutline(square_border_color)
        return square_graphical_object
    
    def open(self):
        self.__is_revealed = True
        is_mine = self.get_is_mine()
        if is_mine:
            self.set_fill_color("red")
        else:
            self.set_fill_color("green")
        self.redraw()
        if self.get_number() > 0:
            h_size = self.__size // 2
            Text(Point(self.__top_left_x + h_size, self.__top_left_y + h_size), self.get_number()).draw(self.__win)
    
    def redraw(self) -> None:
        self.__square_graphical_object.undraw()
        if self.__is_selected:
            self.set_border_color("turquoise")
        else:
            self.set_border_color("black")
        self.__square_graphical_object.draw(self.__win)

    def get_is_mine(self) -> bool:
        return self.__is_mine
    
    def get_top_left_point(self) -> Point:
        return self.__square_graphical_object.getP1()
    
    def get_is_revealed(self) -> bool:
        return self.__is_revealed
    
    def get_number(self) -> int:
        return self.__number
    
    def is_selected(self) -> bool:
        return self.__is_selected
    
    # Note: set methods do not redraw the square, this must be done seperately
    def set_fill_color(self, new_color: str) -> None:
        self.__square_graphical_object.setFill(new_color)

    def set_border_color(self, new_color: str) -> None:
        self.__square_graphical_object.setOutline(new_color)

    def set_number(self, new_number: int) -> None:
        self.__number = new_number

    def select(self):
        self.__is_selected = True
        self.redraw()
    
    def deselect(self):
        self.__is_selected = False
        self.redraw()


def main() -> None:
    play_again = True
    while play_again:
    # Define board parameters
    # Instantiate board
    # Gameplay loop
        game_object = Game()
        game_object.instantiate_board(
            board_size= 700,
            num_squares= 16,
            mine_chance= 0.1
            )
        score = game_object.main_loop()
        play_again = game_object.game_over_screen(score)
        game_object.close_window()


if __name__ == '__main__':
    main()