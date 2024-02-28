import random
import time
from prettytable import PrettyTable
from os import system


# generate field
class Field:

    def __init__(self, n):
        self._n = n
        self._field = [["_" for x in range(self._n)] for y in range(self._n)]

    def _print_field(self):
        table = PrettyTable(align = "c", padding_width = 1, border = False)
        table.field_names = [" ", *range(0,self._n)]

        row = 0
        for line in self._field:
            arr_row = [row, *line]
            table.add_row(arr_row)
            row += 1 
        print(table)

    def _valid_coord(self, x, y):
        return 0 <= x <= self._n - 1 and 0 <= y <= self._n - 1

# field with mines 
class Mines(Field):

    # n = size of field
    # count_of_mines = count of mines on field
    # startx = index of start shoot in line x
    # starty = index of start shoot in line y
    def __init__(self, n: int, count_of_mines: int, startx: int, starty: int):
        
        super().__init__(n)
        if count_of_mines > self._n**2 - 1:
            self.__count_of_mines = int(self._n**2 / 2)
        else:
            self.__count_of_mines = count_of_mines

        self.__startx = startx
        self.__starty = starty
        if self.__count_of_mines < int(self._n**2 / 2):
            self.__generate_bombs_1()
        else:
            self.__generate_bombs_2()

    def __generate_bombs_1(self):

        val = [*range(self._n)]
        count = self.__count_of_mines

        # fill field bombs
        while count != 0:
            x, y = random.choices(val, k = 2)
            if self._field[y][x] != "X" and (y,x) != (self.__starty,self.__startx):
                self._field[y][x] = "X"
                count -= 1

        # fill field values
        for x in range(self._n):
            for y in range(self._n):
                if self._field[x][y] == "X":
                    continue
                else:
                    self._field[x][y] = self.__count_of_mines_around(x, y)

    # Other implementation of generation bombs
    def __generate_bombs_2(self):

        arr_of_coordinates = []
        for x in range(self._n):
            for y in range(self._n):
                arr_of_coordinates.append([x,y])
        arr_of_coordinates.remove([self.__starty, self.__startx])
        len_arr = len(arr_of_coordinates)
        count = self.__count_of_mines

        # fill field bombs
        while count != 0:
            num = random.randint(0, len_arr)
            print(len_arr,num)
            self._field[arr_of_coordinates[num-1][0]][arr_of_coordinates[num-1][1]] = "X"
            arr_of_coordinates.remove(arr_of_coordinates[num-1])
            len_arr -= 1
            count -= 1

        # fill field values
        for x in range(self._n):
            for y in range(self._n):
                if self._field[x][y] == "X":
                    continue
                else:
                    self._field[x][y] = self.__count_of_mines_around(x, y)

    def __count_of_mines_around(self, x, y):
        count = 0

        for i in range(x-1, x+2):
            for j in range(y-1, y+2):

                if (i == x and j == y) or not(self._valid_coord(x,y)):
                    continue
                elif self._valid_coord(i,j):
                    if self._field[i][j] == "X":
                        count += 1

        return str(count)

class Playground(Field):

    def __init__(self, n, count_of_mines, startx, starty):
        super().__init__(n)
        self.__count_of_mines = count_of_mines
        self._mines = Mines(n, count_of_mines, startx, starty)
        self.__count_of_shots = 0
        self._lose = False
        self._check_position(startx, starty)
    
    def _check_position(self, x: int, y: int, set_bomb = 0):
        # this is a shot, not set bomb
        if set_bomb == 0 and self._valid_coord(x,y): 
            
            # shot on free position, if it is not a bomb
            if self._mines._field[y][x] != "X" and self._field[y][x] == "_":
                self._field[y][x] = self._mines._field[y][x]
                self.__count_of_shots += 1

                # open positions around zero with coordinates x,y
                if self._field[y][x] == "0":

                    for i in range(x-1, x+2):
                        for j in range(y-1, y+2):
                            if (i == x and j == y) or not(self._valid_coord(i,j)):
                                continue
                            elif self._valid_coord(i, j) and self._field[j][i] == "_":
                                # recursion
                                self._check_position(i, j)
            
            # shot on numbers to open positions around
            elif self._field[y][x] != "X" and self._field[y][x] != "_":
                is_equal = True

                # condition on equal (playground fields == mines fields)
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if (i == x and j == y) or not(self._valid_coord(i,j)):
                            continue
                        elif self._valid_coord(i, j) and self._field[j][i] == "X" and self._field[j][i] != self._mines._field[j][i]:
                            is_equal = False
                
                if is_equal:
                    for i in range(x-1, x+2):
                        for j in range(y-1, y+2):
                            if (i == x and j == y) or not(self._valid_coord(i,j)):
                                continue
                            # else:
                            #     self._field[j][i] = self.mines._field[j][i]
                            elif self._valid_coord(i, j) and self._field[j][i] == "_":
                                self._check_position(i, j)
                else:
                    self._lose = True # end of game, lose
                                
            else:
                self._lose = True # end of game, lose
        
        # set bomb on playground
        elif self._valid_coord(x,y) and self._field[y][x] == "_":
            self._field[y][x] = "X"

        # del bomb on playground
        else:
            self._field[y][x] = "_"

    def check_is_win(self) -> bool:        
        return self.__count_of_shots == self._n**2 - self.__count_of_mines

    def win_game(self):
        system('cls||clear')
        print("!!!Congratulations! You won the game!!!\n")
        self._mines._print_field()

    def lose_game(self):
        system('cls||clear')
        print("So sad, you lose the game...\n")
        
        for i in range(self._n):
            for j in range(self._n):
                if self._field[i][j] == "X":
                    self._field[i][j] = "_"

        for i in range(self._n):
            for j in range(self._n):
                if self._mines._field[i][j] == "X":
                    self._field[i][j] = self._mines._field[i][j]
                else:
                    continue
        self._print_field()



# input parameteres for game
n = int(input("Input size of playground (n >= 8): "))
while n < 8:
    n = int(input("Input size of playground (n >= 8): "))
count_of_mines = int(input(f"Count of mines (less {n**2}): "))
startx, starty = map(int, input("Start shot x.y: ").split("."))

# create game
game = Playground(n, count_of_mines, startx, starty)
time_of_game = time.time()

# shooting at positions, while game is not end
while True:

    system('cls||clear')
    while True:
        try:
            # !!!CHEATS!!!
            # game._mines._print_field()
            # print("")

            game._print_field()
            print("\nIf you want to plant a bomb, then the parameter should not be equal to 0 and an integer")
            x, y, bomb = map(int, input("Shot position or set bomb (x.y.bomb): ").split("."))
            break
        except ValueError:
            system('cls||clear')
            print("!!!NOT CORRECT INPUT!!! Try again shot position")

    game._check_position(x, y, bomb)
    
    # check for win or lose
    if game.check_is_win():
        game.win_game()
        print("\n",f"Parameteres: size {n}, count of bombs {count_of_mines}")
        print(f"Time of game: {time.time() - time_of_game} sec")
        break
    elif game._lose:
        game.lose_game()
        print("\n",f"Time of game: {time.time() - time_of_game} sec")
        break