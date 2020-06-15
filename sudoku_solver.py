import copy


class Sudoku:

    """
    Class for solving every 9x9 Sudoku.

    Args:
        sudoku (list): Takes a list of rows containing numbers from 0 to 9. 0 is interpreted as an empty cell.
        only_one_solution (boolean): In case of multiple solutions only one valid solution will be calculated if set to
                                     True. Defaults to True.
    Raises:
        ValueError: invalid grid
        ValueError: unsolvable sudoku
    """

    def __init__(self, sudoku, only_one_solution=True):
        self.sudoku = sudoku
        self.only_one_solution = only_one_solution
        self.solutions = list()
        self.cols_candidates = list()
        self.rows_candidates = list()
        self.blocks_candidates = list()
        self.empty_cells = list()

        if len(self.sudoku) != 9:
            raise ValueError('Invalid grid.')
        for row in self.sudoku:
            if len(row) != 9:
                raise ValueError('Invalid grid.')

        for _ in range(9):
            self.cols_candidates.append(set(range(1, 10)))
            self.rows_candidates.append(set(range(1, 10)))
            self.blocks_candidates.append(set(range(1, 10)))

        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0:
                    self.empty_cells.append((i, j, self._pos_to_block(i, j)))
                else:
                    try:
                        self._delete_candidate(i, j, self.sudoku[i][j])
                    except KeyError:
                        raise ValueError('Unsolvable Sudoku.')

    @staticmethod
    def _pos_to_block(i, j):
        return (i // 3) * 3 + (j // 3)

    def _delete_candidate(self, i, j, candidate):
        self.rows_candidates[i].remove(candidate)
        self.cols_candidates[j].remove(candidate)
        self.blocks_candidates[self._pos_to_block(i, j)].remove(candidate)

    def _set_cell(self, pos, value):
        row, col, _ = pos
        self.sudoku[row][col] = value
        self._delete_candidate(row, col, value)
        self.empty_cells.remove(pos)

    def _clear_cell(self, pos, value):
        row, col, block = pos
        self.sudoku[row][col] = 0
        self.rows_candidates[row].add(value)
        self.cols_candidates[col].add(value)
        self.blocks_candidates[block].add(value)
        self.empty_cells.append(pos)

    def _find_best_cell(self):
        count_candidates, best_cell = 10, None
        for pos in self.empty_cells:
            row, col, block = pos
            candidates = self.rows_candidates[row] & self.cols_candidates[col] & self.blocks_candidates[block]
            if len(candidates) < count_candidates:
                best_cell = (pos, candidates)
                count_candidates = len(candidates)
        return best_cell

    def _solve(self):
        if not self.empty_cells:
            return
        pos, candidates = self._find_best_cell()
        for candidate in candidates:
            self._set_cell(pos, candidate)
            if not self.empty_cells:
                self.solutions.append(copy.deepcopy(self.sudoku))
                if self.only_one_solution:
                    return
            self._solve()
            if self.solutions and self.only_one_solution:
                break
            self._clear_cell(pos, candidate)

    def solve(self):
        self._solve()
        if not self.solutions:
            raise ValueError('Unsolvable Sudoku.')
        if self.only_one_solution:
            return self.solutions[0]
        else:
            return self.solutions
