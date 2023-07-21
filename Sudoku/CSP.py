import time
from backtracking import Sudoku


class CSP(Sudoku):
    def __init__(self, dim, fileDir) -> None:
        super().__init__(dim)
        with open(fileDir) as f:
            content = f.readlines()
            self.board = [list(x.strip().split()) for x in content]
        self.rv = self.getRemainingValues()

    def getRemainingValues(self):
        RV = []
        for row in range(self.dim):
            for col in range(self.dim):
                if self.board[row][col] != '0':
                    RV.append(['x'])
                else:
                    RV.append(self.getDomain(row, col))
        return RV

    def getDomain(self, row, col):
        RVCell = [str(i) for i in range(1, self.dim + 1)]
        for i in range(self.dim):
            if self.board[row][i] != '0':
                if self.board[row][i] in RVCell:
                    RVCell.remove(self.board[row][i])
        for j in range(self.dim):
            if self.board[j][col] != '0':
                if self.board[j][col] in RVCell:
                    RVCell.remove(self.board[j][col])
        boxRow = row - row%3
        boxCol = col - col%3
        for i in range(3):
            for j in range(3):
                if self.board[boxRow + i][boxCol + j] != '0':
                    if self.board[boxRow + i][boxCol + j] in RVCell:
                        RVCell.remove(self.board[boxRow + i][boxCol + j])
        return RVCell

    def getNextLocation(self):
        idx = -1
        length = 100
        for i in range(len(self.rv)):
            if self.rv[i] != ['x'] and len(self.rv[i]) < length:
                idx = i
                length = len(self.rv[i])
        if idx == -1:
            return (-1, -1, [])
        x = int(idx / 9)
        y = idx % 9
        return (x, y, self.rv[idx])

    # def solveCSPBackTracking(self):
    #     assign_all_variable = True
    #     for i in range(len(self.rv)):
    #         if self.rv[i] != ['x']:
    #             assign_all_variable = False
    #             x = int(i/9)
    #             y = i % 9
    #             domain = self.rv[i]
    #     if assign_all_variable:
    #         return True
    #     else:
    #         self.expandedNodes += 1
    #         for choice in domain:
    #             self.board[x][y] = choice
    #             self.rv = self.getRemainingValues()
    #             if self.solveCSPBackTracking():
    #                 return True
    #             self.board[x][y] = '0'

    def solveCSPBackTracking(self):
        location = self.getNextLocation()
        x = location[0]
        y = location[1]
        domain = location[2]
        if x == -1:
            return True
        elif len(domain) == 0:
            return False
        else:
            occurrence = {x : 0 for x in domain}
            for d in self.board:
                for number in d:
                    if number in domain:
                        occurrence[number] += 1
            domain.sort(key=lambda x : occurrence[x], reverse=True)
            self.expandedNodes += 1
            for choice in domain:
                self.board[x][y] = choice
                self.rv = self.getRemainingValues()
                if self.solveCSPBackTracking():
                    return True
                self.board[x][y] = '0'


def main():
    sudoku = CSP(9, './sudoku2.txt')
    start = time.time()
    sudoku.solveCSPBackTracking()
    print(f"time: {int(1000 * (time.time() - start))}")
    print(sudoku.expandedNodes)
    sudoku.display()


if __name__ == "__main__":
    main()