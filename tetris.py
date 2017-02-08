from tetromino import Tetromino
from time import sleep
import json
import os
import sys

from collections import namedtuple
ActionReport = namedtuple("ActionReport", "board done score score_from_action")

class Tetris(object):   
    def __init__(self):
        self.start()

    def start(self):
        self.board = self.empty_board()
        self.piece = self.random_piece()
        self.lines_scored = []
        self.is_running = True

    def empty_board(self):
        board = []
        for y in range(20):
            row = []
            for x in range(10):
                row.append(0)
            board.append(row)

        return board

    def print_board(self):
        piece_indices = []
        for row_i, row in enumerate(self.piece.rotations[self.piece.current]):
            for col_i, col in enumerate(row):
                if col == 1:
                    piece_indices.append((col_i + self.piece.x, row_i + self.piece.y))

        board = ""
        for row_i, row in enumerate(self.board):
            board += "\n"
            for col_i, col in enumerate(row):
                n = 0
                if (col_i, row_i) in piece_indices:
                    n += 1

                board += str(col + n)
                board += " "

        return board

    def freeze_current_piece(self):
        for row_i, row in enumerate(self.piece.rotations[self.piece.current]):
            for col_i, col in enumerate(row):
                if col == 1:
                    self.board[row_i + self.piece.y][col_i + self.piece.x] = 1

        lines_cleared = 0
        for row_i, row in enumerate(self.board):
            if all(col == 1 for col in row):
                lines_cleared += 1
                self.board.pop()
                self.board.insert(0, [0 for _ in range(10)])


        if lines_cleared:
            self.lines_scored.append(lines_cleared)

        self.piece = self.random_piece()

        return lines_cleared


    def random_piece(self):
        return Tetromino.random()

    def rotate_piece(self):
        new_current = (self.piece.current + 1) % len(self.piece.rotations)

        x, y = self.piece.x, self.piece.y

        for row_i, row in enumerate(self.piece.rotations[new_current]):
            for col_i, col in enumerate(row):
                if col == 1:
                    if row_i + y >= len(self.board):
                        return False

                    if col_i + x < 0:
                        return False

                    if col_i + x >= len(self.board[0]):
                        return False


        for row_i, row in enumerate(self.piece.rotations[new_current]):
            for col_i, col in enumerate(row):
                if col == 1:

                    if row_i >= len(self.board) - 1:
                        return False

                    if self.board[row_i + y][col_i + x] == 1:
                        return False

        self.piece.current = new_current

        return True

    def move_piece(self, direction):
        if not self.is_running:
            raise Exception("You must start a game before you can move")
        
        x, y = self.piece.x, self.piece.y

        if direction == 'up':
            self.rotate_piece()
        elif direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        elif direction == 'down':
            y += 1
        else:
            raise Exception(direction + " is not a valid command")

        for row_i, row in enumerate(self.piece.rotations[self.piece.current]):
            for col_i, col in enumerate(row):
                if col == 1:
                    if row_i + y >= len(self.board):
                        score_from_freeze = self.freeze_current_piece()
                        return ActionReport(board=self.board, done=False, score=sum(self.lines_scored), score_from_action=score_from_freeze)

                    if col_i + x < 0:
                        return ActionReport(board=self.board, done=False, score=sum(self.lines_scored), score_from_action=0)

                    if col_i + x >= len(self.board[0]):
                        return ActionReport(board=self.board, done=False, score=sum(self.lines_scored), score_from_action=0)


        for row_i, row in enumerate(self.piece.rotations[self.piece.current]):
            for col_i, col in enumerate(row):
                if col == 1:
                    if row_i >= len(self.board) - 1:
                        return ActionReport(board=self.board, done=False, score=sum(self.lines_scored), score_from_action=0)

                    if self.board[row_i + y][col_i + x] == 1:
                        if self.piece.y == 0:
                            self.is_running = False
                            return ActionReport(board=self.board, done=True, score=sum(self.lines_scored), score_from_action=0)
                        else:
                            score_from_freeze = self.freeze_current_piece()
                            return ActionReport(board=self.board, done=False, score=sum(self.lines_scored), score_from_action=score_from_freeze)

        self.piece.x, self.piece.y = x, y

        return ActionReport(board=self.board, done=False, score=sum(self.lines_scored), score_from_action=0)


if __name__ == "__main__":
    scores = []
    game = Tetris()

    moves = [
            'left',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'right',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'right',
            'right',
            'right',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'right',
            'right',
            'right',
            'right',
            'right',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'down',
            'right',
            'right',
            'right',
            'right',
            'right',
            'right',
            'right',
            'right',
            'right',
            'right',
            'right',
            'right',
    ]

    reports = []
    for _ in range(10000):
        for move in moves:
            # print game.print_board()
            # print sum(game.lines_scored)
            # sleep(0.01)

            next_move = move
            if next_move:
                report = game.move_piece(next_move)
                if report.done:
                    reports.append(str(report))
                    game.start()

            report = game.move_piece('down')
            if report.done:
                reports.append(str(report))
                game.start()


            # os.system('clear')

    # print reports

    sys.exit(0)

