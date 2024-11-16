#!/usr/bin/env python3

import chess
import chess.pgn
import sys

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} pgn')
    sys.exit(1)

pgn = open(sys.argv[1])
infile = open('7P-SYZYGY-SUM', 'r')
outfile = open('7P-SYZYGY-FREQ', 'w')

tbs = {}

i = 0
while True:
    i += 1
    print(f'Starting {i}')
    game = chess.pgn.read_game(pgn)
    if game is None:
        break
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        numpieces = len(board.piece_map())

        if numpieces < 7:
            break
        if numpieces == 7:
            whitepieces = ''
            blackpieces = ''
            for c in 'KQRBNP':
                for sq in board.pieces(chess.Piece.from_symbol(c).piece_type, chess.WHITE):
                    whitepieces += c
            for c in 'KQRBNP':
                for sq in board.pieces(chess.Piece.from_symbol(c).piece_type, chess.BLACK):
                    blackpieces += c
            tbstr = ''
            if len(whitepieces) > len(blackpieces):
                tbstr = whitepieces + 'v' + blackpieces
            else:
                tbstr = blackpieces + 'v' + whitepieces
            if tbstr in tbs:
                tbs[tbstr] += 1
            else:
                tbs[tbstr] = 1
            break

total = 0
for val in tbs.values():
    total += val

for line in infile:
    line = line.strip().split(' ')
    tb = line[0]
    byte = line[1]
    freq = 0
    if tb in tbs:
        freq = tbs[tb]
    outfile.write(f'{tb} {byte} {100 * freq / total:.3f}\n')
