from random import randint


class Game:

    def __init__(self):
        self.__score_values = {3: 170, 4: 240, 5: 310, 6: 380, 7: 450, 8: 520}
        self.arr = [[randint(1, 6) for j in range(8)] for i in range(8)]
        self.__update_arr()

    @property
    def arr(self):
        return self._arr

    @arr.setter
    def arr(self, value):
        self._arr = value

    def swap_heart(self, row1: int, col1: int, row2: int, col2: int) -> int:
        """swap elements of array if they placed on the same column or row, and distance between them equals 1"""
        sum_score = 0
        if abs(row1 - row2) + abs(col1 - col2) == 1:
            Game.swap(row1, col1, row2, col2, self.arr)
            sum_score = self.__update_arr()

        if sum_score == 0:
            Game.swap(row1, col1, row2, col2, self.arr)
            return 0
        else:
            return sum_score + self.__update_arr()

    def __update_arr(self) -> int:
        """update array of numbers, return the score of updating values"""
        cur_score = 1
        sum_score = 0
        while cur_score != 0:
            cur_score = self.__delete_duplicates(False) + self.__delete_duplicates(True)
            sum_score += cur_score
            for col in range(len(self.arr[0])):
                self.__fill_empty_cell(col, self.arr)

        return sum_score

    def __delete_duplicates(self, is_row: bool) -> int:
        """delete duplicates in rows or columns, accumulate score"""
        sum_score = 0
        for cur_index in range(len(self.arr[0])):
            iterate_index = 0
            prev = Game.element(is_row, cur_index, iterate_index, self.arr)
            size = 0
            while iterate_index < len(self.arr):
                while iterate_index < len(self.arr) and \
                        Game.element(is_row, cur_index, iterate_index, self.arr) == prev:
                    size += 1
                    prev = Game.element(is_row, cur_index, iterate_index, self.arr)
                    iterate_index += 1

                if size >= 3:
                    for clear_index in range(iterate_index - 1, iterate_index - size - 1, -1):
                        self.__clear_element(is_row, cur_index, clear_index)
                    sum_score += self.__score_values[size]
                if iterate_index < len(self.arr):
                    prev = Game.element(is_row, cur_index, iterate_index, self.arr)
                size = 0
        return sum_score

    def __clear_element(self, is_row: bool, cur_index: int, iterate_index: int):
        """replace elements with zeros"""
        if is_row:
            self.arr[cur_index][iterate_index] = 0
        else:
            self.arr[iterate_index][cur_index] = 0

    @staticmethod
    def element(is_row: bool, cur_index: int, iterate_index: int, arr: [[]]):
        """return the current element on row or column"""
        return arr[cur_index][iterate_index] if is_row else arr[iterate_index][cur_index]

    def __fill_empty_cell(self, cur_index: int, arr: [[]]):
        """move empty cell to begin of column, and then reinitialize they with random values"""
        iterate_index = 0
        while iterate_index < len(arr):
            if arr[iterate_index][cur_index] == 0:
                self.__move_empty_cell(cur_index, iterate_index)
            iterate_index += 1

        for col in range(len(arr[0])):
            for row in range(len(arr)):
                if arr[row][col] == 0:
                    arr[row][col] = randint(1, 6)

    @staticmethod
    def swap(row1: int, col1: int, row2: int, col2: int, arr: [[]]):
        """swap elements in array"""
        arr[row1][col1], arr[row2][col2] = arr[row2][col2], arr[row1][col1]

    def __move_empty_cell(self, row: int, col: int):
        """move empty cell to begin of column"""
        if row == 0 or self.arr[row - 1][col] == 0:
            return
        self.swap(row, col, row - 1, col, self.arr)
        self.__move_empty_cell(row - 1, col)
