

import time


class Sudoku:
    def __init__(self, dim) -> None:
        self.dim = dim
        self.expandedNodes = 0
        # self.board = [['0' for i in range(self.dim)] for j in range(self.dim)]
        with open('./sudoku2.txt') as f:
            content = f.readlines()
            self.board = [list(x.strip().split()) for x in content]

    def solveSimpleBackTracking(self):
        location = self.getNextLocation()
        x = location[0]
        y = location[1]
        if x == -1:
            return True
        else:
            self.expandedNodes += 1
            for choice in range(1, self.dim + 1):
                if self.isSafe(x, y, choice):
                    self.board[x][y] = str(choice)
                    if self.solveSimpleBackTracking():
                        return True
                    self.board[x][y] = '0'
        return False

    def getNextLocation(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.board[x][y] == '0':
                    return (x, y)
        return (-1, -1)

    def isSafe(self, x, y, value):
        for i in range(self.dim):
            if self.board[x][i] == str(value):
                return False
        for i in range(self.dim):
            if self.board[i][y] == str(value):
                return False
        boxRow = x - x%3
        boxCol = y - y%3
        for i in range(3):
            for j in range(3):
                if self.board[boxRow + i][boxCol + j] == str(value):
                    return False
        return True

    def display(self):
        for i in range(self.dim):
            row = ""
            for j in range(self.dim):
                if j % 3 == 2:
                    row += f"{self.board[i][j]}   |   "
                else:
                    row += f"{self.board[i][j]}\t"
            if i % 3 == 0:
                print(18 * "-   ")
            row += '\n'
            print(row)


def main():
    sudoku = Sudoku(9)
    start = time.time()
    sudoku.solveSimpleBackTracking()
    print(f"time: {int(1000 * (time.time() - start))}")
    print(sudoku.expandedNodes)
    # sudoku.display()


if __name__ == "__main__":
    main()


