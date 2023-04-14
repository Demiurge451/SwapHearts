from random import randint

score = {3: 170, 4: 240, 5: 310, 6: 380, 7: 450, 8: 520}


def swap_heart(row1: int, col1: int, row2: int, col2: int, arr: [[]]) -> int:
    sum_score = 0
    if abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1:
        swap(row1, col1, row2, col2, arr)
        sum_score = update_grid(arr)
        if sum_score == 0:
            swap(row1, col1, row2, col2, arr)

    return sum_score


def update_grid(arr: [[]]) -> [[]]:
    cur_score = 1
    sum_score = 0
    while cur_score != 0:
        cur_score = delete_duplicates(False, arr) + delete_duplicates(True, arr)
        sum_score += cur_score
        for col in range(len(arr[0])):
            fill_empty_cell(col, arr)

    return sum_score


# TODO add score realization
def delete_duplicates(isRow: bool, arr: [[]]) -> int:
    """delete duplicates in rows or columns, accumulate score"""
    sum_score = 0
    for cur_index in range(len(arr[0])):
        iterate_index = 0
        prev = element(isRow, cur_index, iterate_index, arr)
        size = 0
        while iterate_index < len(arr):
            while iterate_index < len(arr) and element(isRow, cur_index, iterate_index, arr) == prev:
                size += 1
                prev = element(isRow, cur_index, iterate_index, arr)
                iterate_index += 1

            if size >= 3:
                for clear_index in range(iterate_index - 1, iterate_index - size - 1, -1):
                    clear_element(isRow, cur_index, clear_index, arr)
                sum_score += score[size]
            if iterate_index < len(arr):
                prev = element(isRow, cur_index, iterate_index, arr)
            size = 0
    return sum_score


def clear_element(isRow: bool, curIndex: int, iterate_index: int, arr: [[]]):
    if isRow:
        arr[curIndex][iterate_index] = 0
    else:
        arr[iterate_index][curIndex] = 0


def element(isRow: bool, cur_index: int, iterate_index: int, arr: [[]]):
    """return the current element on row or column"""
    return arr[cur_index][iterate_index] if isRow else arr[iterate_index][cur_index]


# TODO add diapason
def fill_empty_cell(cur_index: int, arr: [[]]):
    """move empty cell to begin of column, and then reinitialize they with random values"""
    iterate_index = 0
    while iterate_index < len(arr):
        if arr[iterate_index][cur_index] == 0:
            move_empty_cell(cur_index, iterate_index, arr)
        iterate_index += 1

    for col in range(len(arr[0])):
        for row in range(len(arr)):
            if arr[row][col] == 0:
                # diapason of random [1, 6]
                arr[row][col] = randint(1, 6)


def swap(row1: int, col1: int, row2: int, col2: int, arr: [[]]):
    """swap elements in array"""
    arr[row1][col1], arr[row2][col2] = arr[row2][col2], arr[row1][col1]


def move_empty_cell(row: int, col: int, arr: [[]]):
    """move empty cell to begin of column"""
    if row == 0 or arr[row - 1][col] == 0:
        return
    swap(row, col, row - 1, col, arr)
    move_empty_cell(row - 1, col, arr)
