import random
from copy import deepcopy

blocks = {1: [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 2), (1, 2), (2, 2), (3, 2)], [(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)]],
          2: [[(0, 0), (1, 0), (0, 1), (0, 2)], [(-1, 1), (0, 1), (1, 1), (1, 2)], [(1, 0), (1, 1), (1, 2), (0, 2)], [(-1, 0), (-1, 1), (0, 1), (1, 1)]],
          3: [[(0, 0), (0, 1), (0, 2), (1, 2)], [(-1, 1), (-1, 2), (0, 1), (1, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)], [(1, 0), (1, 1), (0, 1), (-1, 1)]],
          4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)]],
          5: [[(0, 0), (0, 1), (1, 1), (1, 2)], [(0, 1), (1, 1), (0, 2), (-1, 2)], [(0, 0), (0, 1), (1, 1), (1, 2)], [(2, 0), (1, 0), (1, 1), (0, 1)]],
          6: [[(0, 0), (0, 1), (0, 2), (1, 1)], [(-1, 1), (0, 1), (0, 2), (1, 1)], [(0, 0), (0, 1), (0, 2), (-1, 1)], [(0, 0), (0, 1), (-1, 1), (1, 1)]],
          7: [[(1, 0), (1, 1), (0, 1), (0, 2)], [(-1, 1), (0, 1), (0, 2), (1, 2)], [(1, 0), (1, 1), (0, 1), (0, 2)], [(0, 0), (1, 0), (1, 1), (2, 1)]]}


class GameState():
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(22)]
        self.block_type = 0
        self.block_coordinates = [0, 0]
        self.block_rotation = 0
        self.stats = {'blocks_dropped': 0, 'lines_cleared': 0, 'tetrises': 0}
        self.spawn_new_block()
        self.print_board()

    def spawn_new_block(self):
        self.block_type = random.randint(1, 7)
        self.block_coordinates = [19, 4]
        self.stats['blocks_dropped'] += 1

    def write_block_to_board(self, board):
        block_coords = blocks[self.block_type][self.block_rotation]
        i, j = self.block_coordinates
        for diff_i, diff_j in block_coords:
            board[i + diff_i][j + diff_j] = self.block_type
        return board

    def print_board(self):
        temp_board = deepcopy(self.board)
        temp_board = self.write_block_to_board(temp_board)
        print('+' + '-' * 21 + '+')
        for i in range(19, -1, -1):
            row_print = '| '
            for char in temp_board[i]:
                row_print += f'{char} '
            row_print += '|'
            if i == 15:
                row_print += ' ' * 5 + 'Blocks dropped:'
            if i == 14:
                row_print += f"{' ' * 5}{self.stats['blocks_dropped']}"
            if i == 12:
                row_print += ' ' * 5 + 'Lines cleared:'
            if i == 11:
                row_print += f"{' ' * 5}{self.stats['lines_cleared']}"
            if i == 9:
                row_print += ' ' * 5 + 'Tetrises:'
            if i == 8:
                row_print += f"{' ' * 5}{self.stats['tetrises']}"
            print(row_print)
        print('+' + '-' * 21 + '+')

    def clear_rows(self, rows):
        to_be_cleared = []
        for row in rows:
            if all([val != 0 for val in self.board[row]]):
                to_be_cleared.append(row)
        for row in sorted(to_be_cleared, reverse=True):
            self.board.append([0] * 10)
            del self.board[row]
            self.stats['lines_cleared'] += 1
        if len(to_be_cleared) == 4:
            self.stats['tetrises'] += 1

    def drop_block(self):
        i, j = self.block_coordinates
        rows = {i + x for x, _ in blocks[self.block_type][self.block_rotation]}
        for diff_i, diff_j in blocks[self.block_type][self.block_rotation]:
            if self.board[i + diff_i - 1][j + diff_j] != 0 or i + diff_i == 0:
                # comes to rest
                self.write_block_to_board(self.board)
                self.clear_rows(rows)
                self.spawn_new_block()
                break
        # falls 1 unit
        self.block_coordinates[0] -= 1

    def push_block(self, input):
        direction_bit = 0
        i, j = self.block_coordinates
        if input == 'D':
            direction_bit += 1
        elif input == 'A':
            direction_bit -= 1
        for diff_i, diff_j in blocks[self.block_type][self.block_rotation]:
            destination_column = j + diff_j + direction_bit
            if destination_column < 0 or destination_column >= 10 or self.board[i + diff_i][destination_column] != 0:
                return
        self.block_coordinates[1] += direction_bit

    def rotate_block(self):
        self.block_rotation = (self.block_rotation + 1) % 4
        # TODO: figure out logic for rotation based collosions

    def get_next_state(self, input):
        if input == 'S':
            self.drop_block()
        elif input in ['A', 'D']:
            self.push_block(input)
        elif input == 'W':
            self.rotate_block()
        self.print_board()
        return self.board


NewGame = GameState()
print("Type moves (A/S/D) or [T]erminate.")
playing = True
while playing:
    move = input()
    if move == 'T':
        playing = False
        break
    NewGame.get_next_state(move)
print('Goodbye!')
